from __future__ import absolute_import, unicode_literals

import datetime
import json
import os
import subprocess
import tempfile
import traceback
from pathlib import Path
from shutil import copy, move, rmtree
from zipfile import ZipFile

from celery import shared_task
from core.settings import (
    DOWNLOAD_DIR,
    DVC_REMOTE_PATH,
    GIT_REMOTE_PATH,
    IMAGE_HASH_MAPPING_URL,
    REPOSITORY_DIR,
    THUMBNAILS_DIR,
    UPLOAD_DIR,
)
from weedcoco.index.indexing import ElasticSearchIndexer
from weedcoco.index.thumbnailing import thumbnailing
from weedcoco.repo.deposit import Repository, RepositoryError, deposit, mkdir_safely
from weedcoco.repo.repository import ensure_ocfl, migrate_dir

from weedid.models import Dataset, WeedidUser
from weedid.notification import (
    edit_notification,
    review_notification,
    upload_notification,
)
from weedid.utils import make_upload_entity_fields


@shared_task
def submit_upload_task(weedcoco_path, image_dir, upload_id, mode="upload"):
    """Submit deposit task from upload

    Parameters
    ----------
    weedcoco_path : str
    image_dir : str
    upload_id : str
    mode : str ("upload"|"edit"|"admin")
    """
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    with open(weedcoco_path) as f:
        weedcoco = json.load(f)
    if mode == "upload":
        upload_entity.status = "P"
        upload_entity.status_details = ""
        upload_entity.save()
        # Update fields in database
        # XXX: maybe this should be delayed
        for k, v in make_upload_entity_fields(weedcoco).items():
            setattr(upload_entity, k, v)
    elif mode == "admin":
        weedcoco["info"]["metadata"] = upload_entity.metadata
        weedcoco["agcontexts"] = upload_entity.agcontext
        with open(weedcoco_path, "w") as f:
            json.dump(weedcoco, f)
    elif mode == "edit":
        pass

    upload_entity.save()
    user = WeedidUser.objects.get(id=upload_entity.user_id)
    metadata = {
        "name": user.username,
        "address": user.email,
        "message": "WeedAI upload",
    }
    try:
        deposit(
            Path(weedcoco_path),
            Path(image_dir),
            Path(REPOSITORY_DIR),
            Path(DOWNLOAD_DIR),
            metadata,
            upload_id,
            IMAGE_HASH_MAPPING_URL,
        )
    except Exception as e:
        traceback.print_exc()
        if mode == "upload":
            upload_entity.status = "F"
            upload_entity.status_details = str(e)
            upload_entity.save()
        elif mode == "edit":
            edit_notification("unsuccessful during depositing", upload_id)
        elif mode == "admin":
            move(
                str(
                    Path(UPLOAD_DIR)
                    / str(upload_entity.user_id)
                    / upload_id
                    / f"{upload_id}.zip"
                ),
                DOWNLOAD_DIR,
            )
            # rolling back the OCFL repo is done in deposit now
            # move(
            #     str(Path(UPLOAD_DIR) / str(upload_entity.user_id) / upload_id),
            #     str(Path(REPOSITORY_DIR) / upload_id),
            # )
            raise
    else:
        if mode == "upload":
            upload_notification(upload_id)
            upload_entity.status = "AR"
            upload_entity.status_details = "It is currently under review."
            upload_entity.save()
        elif mode in ("edit", "admin"):
            if upload_entity.status == "C":
                reindex_dataset.delay(upload_id, mode=mode)
                return


@shared_task
def update_index_and_thumbnails(
    upload_id,
    process_thumbnails=True,
    thumbnails_dir=THUMBNAILS_DIR,
    repository_dir=REPOSITORY_DIR,
    mode="upload",
):
    """Submit deposit task from upload

    Parameters
    ----------
    upload_id : str
    process_thumbnails: bool, default=True
    thumbnails_dir: str, default=THUMBNAILS_DIR
    repository_dir: str, default=REPOSITORY_DIR
    mode : str ("upload"|"edit"|"admin")
    """
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    repository = Repository(Path(repository_dir))
    dataset = repository.dataset(upload_id)
    try:
        if not dataset.exists_in_repo:
            raise RepositoryError(f"Dataset {upload_id} not found in repository")
        weedcoco_path = dataset.resolve_path("weedcoco.json")
        if process_thumbnails:
            # The thumbnails need to be present before indexing
            thumbnailing(Path(thumbnails_dir), Path(repository_dir), upload_id)
        es_index = ElasticSearchIndexer(
            Path(weedcoco_path),
            Path(thumbnails_dir),
            es_host="elasticsearch",
            es_port=9200,
            upload_id=upload_id,
            version_id=dataset.head_version,
        )
        es_index.post_index_entries()
    except Exception as e:
        traceback.print_exc()
        if mode == "upload":
            upload_entity.status = "F"
            upload_entity.status_details = str(e)
        elif mode == "edit":
            edit_notification("unsuccessful during indexing", upload_id)
        elif mode == "admin":
            raise
    else:
        if mode == "upload":
            upload_entity.status = "C"
            upload_entity.status_details = "It has been successfully indexed."
            review_notification("approved and indexed", upload_id)
        elif mode == "edit":
            with open(weedcoco_path) as f:
                weedcoco = json.load(f)
            for k, v in make_upload_entity_fields(weedcoco).items():
                setattr(upload_entity, k, v)
            edit_notification("successful", upload_id)
        elif mode == "admin":
            return
    finally:
        upload_entity.save()


@shared_task
def reindex_dataset(
    upload_id,
    process_thumbnails=True,
    thumbnails_dir=THUMBNAILS_DIR,
    repository_dir=REPOSITORY_DIR,
    mode="admin",
):
    """Reindex a dataset already in the repository"""
    repository = Repository(repository_dir)
    dataset = repository.dataset(upload_id)
    weedcoco_path = dataset.resolve_path("weedcoco.json")
    with open(weedcoco_path) as f:
        weedcoco = json.load(f)
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    for k, v in make_upload_entity_fields(weedcoco).items():
        setattr(upload_entity, k, v)
    upload_entity.head_version = int(dataset.head_version[1:])
    upload_entity.save()
    update_index_and_thumbnails.delay(
        upload_id,
        process_thumbnails=process_thumbnails,
        thumbnails_dir=str(thumbnails_dir),
        repository_dir=str(repository_dir),
        mode=mode,
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
    repository = Repository(repository_dir)
    dataset = repository.dataset(upload_id)
    upload_user_dir = Path(upload_dir) / str(upload_entity.user_id)
    upload_id_dir = upload_user_dir / upload_id
    if os.path.exists(upload_id_dir):
        rmtree(upload_id_dir)
    mkdir_safely(upload_id_dir)
    dataset.extract(upload_id_dir)
    move(str(download_dir / f"{upload_id}.zip"), str(upload_id_dir))
    images_dir = upload_id_dir / "images"
    weedcoco_path = upload_id_dir / "weedcoco.json"
    submit_upload_task.delay(
        str(weedcoco_path), str(images_dir), upload_id, mode="admin"
    )


@shared_task
def remove_dataset(
    upload_id,
    repository_dir=REPOSITORY_DIR,
    download_dir=DOWNLOAD_DIR,
    upload_dir=UPLOAD_DIR,
):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    upload_record_path = Path(upload_dir) / str(upload_entity.user_id) / upload_id
    download_zipfile_path = str(Path(download_dir) / f"{upload_id}.zip")
    repository = Repository(repository_dir)
    dataset = repository.dataset(upload_id)

    # remove upload record
    if os.path.exists(upload_record_path):
        rmtree(upload_record_path)
    # remove download entity
    if os.path.isfile(download_zipfile_path):
        os.remove(download_zipfile_path)
    # remove dataset in repositry
    dataset.remove()
    # remove dataset index
    ElasticSearchIndexer.remove_all_index_with_upload(
        upload_id, es_host="elasticsearch"
    )
    # remove database entity
    if upload_entity:
        upload_entity.delete()


@shared_task
def migrate_to_ocfl(
    old_repository_dir,
    upload_id,
    metadata,
    thumbnails_dir=THUMBNAILS_DIR,
    repository_dir=REPOSITORY_DIR,
):
    repository = ensure_ocfl(repository_dir)
    migrate_dir(repository, Path(old_repository_dir), metadata)
    update_index_and_thumbnails.delay(
        upload_id,
        process_thumbnails=True,
        thumbnails_dir=str(thumbnails_dir),
        repository_dir=str(repository_dir),
        mode="admin",
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


@shared_task
def store_tmp_image_from_zip(upload_id, upload_image_zip, image_dir, full_images):
    if not os.path.isdir(image_dir):
        mkdir_safely(image_dir)
    existing_images = os.listdir(image_dir)
    with tempfile.TemporaryDirectory() as tempdir:
        ZipFile(upload_image_zip).extractall(tempdir)
        for dir, _, filenames in os.walk(tempdir):
            # FIXME: this should reject a zip upload if two filenames are identical
            for filename in filenames:
                if filename in full_images and filename not in existing_images:
                    copy(os.path.join(dir, filename), os.path.join(image_dir, filename))
    missing_images = list(set(os.listdir(image_dir)))
    return {"upload_id": upload_id, "missing_images": missing_images}
