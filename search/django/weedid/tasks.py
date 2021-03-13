from __future__ import absolute_import, unicode_literals
import json
import traceback
from celery import shared_task
from weedcoco.repo.deposit import deposit
from weedcoco.index.indexing import ElasticSearchIndexer
from weedcoco.index.thumbnailing import thumbnailing
from weedid.models import Dataset
from weedid.utils import make_upload_entity_fields
from core.settings import THUMBNAILS_DIR, REPOSITORY_DIR, DOWNLOAD_DIR
from pathlib import Path


@shared_task
def submit_upload_task(weedcoco_path, image_dir, upload_id):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
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
        traceback.print_exc()
        upload_entity.status = "F"
        upload_entity.status_details = str(e)
        upload_entity.save()
    else:
        upload_entity.status = "AR"
        upload_entity.status_details = "It is currently under review."
        upload_entity.save()


@shared_task
def update_index_and_thumbnails(
    weedcoco_path,
    upload_id,
    dataset_name,
    thumbnails_dir=THUMBNAILS_DIR,
    repository_dir=REPOSITORY_DIR,
):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    try:
        thumbnailing(
            Path(thumbnails_dir), Path(repository_dir) / upload_id, weedcoco_path
        )
        es_index = ElasticSearchIndexer(
            Path(weedcoco_path),
            Path(thumbnails_dir),
            dataset_name=dataset_name,
            es_host="elasticsearch",
            es_port=9200,
            upload_id=upload_id,
        )
        es_index.post_index_entries()
    except Exception as e:
        traceback.print_exc()
        upload_entity.status = "F"
        upload_entity.status_details = str(e)
    else:
        upload_entity.status = "C"
        upload_entity.status_details = "It has been successfully submitted."
    finally:
        upload_entity.save()
