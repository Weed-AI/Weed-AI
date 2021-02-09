import pathlib
import pytest

from elasticmock import elasticmock as elasticmock
from weedcoco.index.indexing import main, ElasticSearchIndexer

BASIC_INPUT_PATH = str(
    pathlib.Path(__file__).parent.parent
    / "repo"
    / "deposit_data"
    / "basic_1"
    / "weedcoco.json"
)
THUMBNAIL_DIR = "arbitrary-thumbnail-dir"


@elasticmock
def test_smoke_indexing():
    # run indexing but check nothing
    main(["--weedcoco-path", BASIC_INPUT_PATH, "--thumbnail-dir", THUMBNAIL_DIR])


def test_batch_generation():
    # TODO
    pytest.xfail("Not yet implemented")


def test_task_type():
    indexer = ElasticSearchIndexer(
        weedcoco_path=BASIC_INPUT_PATH, thumbnail_dir=THUMBNAIL_DIR
    )
    for entry in indexer.generate_index_entries():
        assert isinstance(entry["task_type"], list)
    # TODO: test the task type for different input annotation data
    pytest.xfail("Not yet implemented")


def test_annotation_and_category():
    "Check annotations and categories are correctly indexed with each image"
    # TODO
    pytest.xfail("Not yet implemented")


def test_growth_range():
    indexer = ElasticSearchIndexer(
        weedcoco_path=BASIC_INPUT_PATH, thumbnail_dir=THUMBNAIL_DIR
    )
    for entry in indexer.generate_index_entries():
        growth_range = entry["agcontext"]["bbch_growth_range"]
        assert growth_range == [10, 20]
        growth_stage_texts = entry["agcontext"]["growth_stage_texts"]
        assert len(growth_stage_texts) == 2
