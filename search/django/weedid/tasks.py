from __future__ import absolute_import, unicode_literals
from celery import shared_task
from weedcoco.repo.deposit import deposit
from weedcoco.index.indexing import ElasticSearchIndexer
from weedcoco.index.thumbnailing import thumbnailing
from weedid.models import Dataset
from core.settings import THUMBNAILS_DIR, REPOSITORY_DIR, DOWNLOAD_DIR
from pathlib import Path


@shared_task
def submit_upload_task(weedcoco_path, image_dir, upload_id):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    upload_entity.status = "P"
    upload_entity.status_details = ""
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
    thumbnails_dir=THUMBNAILS_DIR,
    repository_dir=REPOSITORY_DIR,
):
    upload_entity = Dataset.objects.get(upload_id=upload_id)
    try:
        es_index = ElasticSearchIndexer(
            Path(weedcoco_path),
            Path(thumbnails_dir),
            es_host="elasticsearch",
            es_port=9200,
            upload_id=upload_id,
        )
        es_index.post_index_entries()
        thumbnailing(Path(thumbnails_dir), Path(repository_dir))
    except Exception as e:
        upload_entity.status = "F"
        print(e)
        upload_entity.status_details = str(e)
    else:
        upload_entity.status = "C"
        upload_entity.status_details = "It has been successfully proceeded."
    finally:
        upload_entity.save()
