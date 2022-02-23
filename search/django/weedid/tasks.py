from __future__ import absolute_import, unicode_literals
import json
import traceback
import datetime
import subprocess
from celery import shared_task
from weedcoco.repo.deposit import deposit, compress_to_download
from weedcoco.index.indexing import ElasticSearchIndexer
from weedcoco.index.thumbnailing import thumbnailing
from weedid.models import Dataset
from weedid.utils import make_upload_entity_fields
from weedid.notification import upload_notification, review_notification
from core.settings import (
    THUMBNAILS_DIR,
    REPOSITORY_DIR,
    DOWNLOAD_DIR,
    UPLOAD_DIR,
    GIT_REMOTE_PATH,
    DVC_REMOTE_PATH,
)
from pathlib import Path
import os
from shutil import move, rmtree


@shared_task
def submit_upload_task(weedcoco_path, image_dir, upload_id, new_upload=True):
    """Submit deposit task from upload

    Parameters
    ----------
    weedcoco_path : str
    image_dir : str
    upload_id : str
    new_upload : bool, default=True
        If it's not a new upload and fails the deposit, updated metadata and agcontexts need to be applied to weedcoco.json and previous deposited dataset and zip file should be copied back when exception raised during deposit.
    """
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    if new_upload:
        upload_entity.status = "P"
        upload_entity.status_details = ""
        upload_entity.save()
        # Update fields in database
        # XXX: maybe this should be delayed
        with open(weedcoco_path) as f:
            weedcoco = json.load(f)
        for k, v in make_upload_entity_fields(weedcoco).items():
            setattr(upload_entity, k, v)
    else:
        with open(weedcoco_path) as f:
            weedcoco = json.load(f)
        weedcoco["info"]["metadata"] = upload_entity.metadata
        weedcoco["agcontexts"] = upload_entity.agcontext
        with open(weedcoco_path, "w") as f:
            json.dump(weedcoco, f)

    upload_entity.save()
    try:
        deposit(
            Path(weedcoco_path),
            Path(image_dir),
            Path(REPOSITORY_DIR),
            Path(DOWNLOAD_DIR),
            upload_id,
        )
    except Exception as e:
        if not new_upload:
            move(
                str(
                    Path(UPLOAD_DIR)
                    / str(upload_entity.user_id)
                    / upload_id
                    / f"{upload_id}.zip"
                ),
                DOWNLOAD_DIR,
            )
            move(
                str(Path(UPLOAD_DIR) / str(upload_entity.user_id) / upload_id),
                str(Path(REPOSITORY_DIR) / upload_id),
            )
            raise
        traceback.print_exc()
        upload_entity.status = "F"
        upload_entity.status_details = str(e)
        upload_entity.save()
        # TODO: raise alert
    else:
        if not new_upload:
            if upload_entity.status == "C":
                reindex_dataset.delay(upload_id)
            return
        upload_notification(upload_id)
        upload_entity.status = "AR"
        upload_entity.status_details = "It is currently under review."
        upload_entity.save()


@shared_task
def update_index_and_thumbnails(
    weedcoco_path,
    upload_id,
    process_thumbnails=True,
    thumbnails_dir=THUMBNAILS_DIR,
    repository_dir=REPOSITORY_DIR,
    new_upload=True,
):
    """Submit deposit task from upload

    Parameters
    ----------
    weedcoco_path : str
    upload_id : str
    process_thumbnails: bool, default=True
    thumbnails_dir: str, default=THUMBNAILS_DIR
    repository_dir: str, default=REPOSITORY_DIR
    new_upload : bool, default=True
        If it's not a new upload, upload status and status details don't need to be updated.
    """
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    try:
        if process_thumbnails:
            # The thumbnails need to be present before indexing
            thumbnailing(
                Path(thumbnails_dir), Path(repository_dir) / upload_id, weedcoco_path
            )
        es_index = ElasticSearchIndexer(
            Path(weedcoco_path),
            Path(thumbnails_dir),
            es_host="elasticsearch",
            es_port=9200,
            upload_id=upload_id,
        )
        es_index.post_index_entries()
    except Exception as e:
        if not new_upload:
            raise
        traceback.print_exc()
        upload_entity.status = "F"
        upload_entity.status_details = str(e)
    else:
        if not new_upload:
            return
        upload_entity.status = "C"
        upload_entity.status_details = "It has been successfully indexed."
        review_notification("approved and indexed", upload_id)
    finally:
        upload_entity.save()


@shared_task
def reindex_dataset(
    upload_id,
    process_thumbnails=True,
    thumbnails_dir=THUMBNAILS_DIR,
    repository_dir=REPOSITORY_DIR,
    download_dir=DOWNLOAD_DIR,
):
    """Reindex a dataset already in the repository, and recreate its download"""
    download_dir = Path(download_dir)
    dataset_dir = Path(repository_dir) / upload_id
    weedcoco_path = dataset_dir / "weedcoco.json"
    with open(weedcoco_path) as f:
        weedcoco = json.load(f)

    upload_entity = Dataset.objects.get(upload_id=upload_id)
    for k, v in make_upload_entity_fields(weedcoco).items():
        setattr(upload_entity, k, v)
    upload_entity.save()

    compress_to_download(dataset_dir, upload_id, download_dir)
    update_index_and_thumbnails.delay(
        str(weedcoco_path),
        upload_id,
        process_thumbnails=process_thumbnails,
        thumbnails_dir=str(thumbnails_dir),
        repository_dir=str(repository_dir),
        new_upload=False,
    )


@shared_task
def redeposit_dataset(
    upload_id,
    repository_dir=REPOSITORY_DIR,
    download_dir=DOWNLOAD_DIR,
    upload_dir=UPLOAD_DIR,
):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    download_dir = Path(download_dir)
    dataset_dir = Path(repository_dir) / upload_id
    upload_user_dir = Path(upload_dir) / str(upload_entity.user_id)
    upload_id_dir = upload_user_dir / upload_id
    if os.path.exists(upload_id_dir):
        rmtree(upload_id_dir)
    move(str(dataset_dir), str(upload_user_dir))
    move(str(download_dir / f"{upload_id}.zip"), str(upload_id_dir))
    images_dir = upload_id_dir / "images"
    weedcoco_path = upload_id_dir / "weedcoco.json"
    submit_upload_task.delay(
        str(weedcoco_path), str(images_dir), upload_id, new_upload=False
    )


@shared_task
def backup_repository_changes(repository_dir=REPOSITORY_DIR, commit_message=None):
    # XXX: Not safe for concurrency
    if commit_message is None:
        commit_message = f"repo updates until {datetime.datetime.now()}"
    assert GIT_REMOTE_PATH, r"GIT_REMOTE_PATH={repr(GIT_REMOTE_PATH)}"
    assert DVC_REMOTE_PATH, r"DVC_REMOTE_PATH={repr(DVC_REMOTE_PATH)}"
    subprocess.check_call(
        [
            "bash",
            Path(__file__).parent / "bin" / "dvc_push.sh",
            GIT_REMOTE_PATH,
            DVC_REMOTE_PATH,
            commit_message,
        ],
        cwd=REPOSITORY_DIR,
    )
