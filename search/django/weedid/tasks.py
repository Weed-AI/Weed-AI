from __future__ import absolute_import, unicode_literals
import json
import traceback
from celery import shared_task
from weedcoco.repo.deposit import deposit, compress_to_download
from weedcoco.index.indexing import ElasticSearchIndexer
from weedcoco.index.thumbnailing import thumbnailing
from weedid.models import Dataset
from weedid.utils import make_upload_entity_fields
from weedid.notification import upload_notification
from core.settings import THUMBNAILS_DIR, REPOSITORY_DIR, DOWNLOAD_DIR
from pathlib import Path


@shared_task
def submit_upload_task(weedcoco_path, image_dir, upload_id, new_upload=True):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    if new_upload:
        upload_entity.status = "P"
        upload_entity.status_details = ""

    # Update fields in database
    # XXX: maybe this should be delayed
    with open(weedcoco_path) as f:
        weedcoco = json.load(f)
    for k, v in make_upload_entity_fields(weedcoco).items():
        setattr(upload_entity, k, v)

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
            raise
        traceback.print_exc()
        upload_entity.status = "F"
        upload_entity.status_details = str(e)
        upload_entity.save()
        # TODO: raise alert
    else:
        if not new_upload:
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
        upload_entity.status_details = "It has been successfully submitted."
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
):
    download_dir = Path(download_dir)
    dataset_dir = Path(repository_dir) / upload_id
    images_dir = dataset_dir / "images"
    weedcoco_path = dataset_dir / "weedcoco.json"
    submit_upload_task.delay(
        str(weedcoco_path), str(images_dir), upload_id, new_upload=False
    )
