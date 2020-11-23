from __future__ import absolute_import, unicode_literals
from celery import shared_task
from weedcoco.repo.deposit import deposit
from weedcoco.index.indexing import ElasticSearchIndex
from weedcoco.index.thumbnailing import thumbnailing
from core.settings import THUMBNAILS_DIR, REPOSITORY_DIR
from pathlib import Path


@shared_task
def upload_task(weedcoco_path, image_dir):
    new_weedcoco_path = deposit(
        Path(weedcoco_path), Path(image_dir), Path(REPOSITORY_DIR)
    )
    update_index_and_thumbnails.delay(new_weedcoco_path)


@shared_task
def update_index_and_thumbnails(
    weedcoco_path, thumbnails_dir=THUMBNAILS_DIR, repository_dir=REPOSITORY_DIR
):
    es_index = ElasticSearchIndex(
        Path(weedcoco_path), Path(thumbnails_dir), es_url="http://elasticsearch:9200/"
    )
    es_index.modify_coco()
    es_index.generate_batches()
    es_index.post_index()
    thumbnailing(Path(thumbnails_dir), Path(repository_dir))
