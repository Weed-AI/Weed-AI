import pathlib
import json
import pytest
import os
import filecmp
import re
from weedcoco.repo.deposit import main
from weedcoco.validation import ValidationError

TEST_DATA_DIR = pathlib.Path(__file__).parent / "deposit_data"
TEST_DATA_SAMPLE_DIR = pathlib.Path(__file__).parent / "deposit_data_sample"
TEST_BASIC_DIR_1 = TEST_DATA_DIR / "basic_1"
TEST_BASIC_DIR_2 = TEST_DATA_DIR / "basic_2"
TEST_COMPLETE_DIR = TEST_DATA_DIR / "complete"
TEST_DUPLICATE_DIR = TEST_DATA_DIR / "duplicate"


@pytest.fixture
def executor(tmpdir):
    test_repo_dir = tmpdir / "test_repo"

    class Executor:
        def run(self, weedcoco_path, image_dir, repository_dir=test_repo_dir):
            args = [
                "--weedcoco-path",
                weedcoco_path,
                "--image-dir",
                image_dir,
                "--repository-dir",
                repository_dir,
            ]
            args = [str(arg) for arg in args]
            main(args)
            return test_repo_dir

    return Executor()


def assert_files_equal(dir1, dir2):

    dirs_cmp = filecmp.dircmp(dir1, dir2, ignore=[".DS_Store"])
    assert len(dirs_cmp.left_only) == 0
    assert len(dirs_cmp.right_only) == 0
    assert len(dirs_cmp.funny_files) == 0
    match, mismatch, errors = filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False
    )
    assert len(mismatch) == 0
    assert len(errors) == 0
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        assert_files_equal(new_dir1, new_dir2)


def assert_weedcoco_equal(dir1, dir2):
    def ordered_json(obj):
        if isinstance(obj, dict):
            return sorted((k, ordered_json(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(ordered_json(x) for x in obj)
        else:
            return obj

    return all(
        [
            ordered_json(json.load(open(dir1 / dir / "weedcoco.json")))
            == ordered_json(json.load(open(dir2 / dir / "weedcoco.json")))
            for dir in os.listdir(dir2)
            if re.fullmatch(r"^dataset_\d+$", dir)
        ]
    )


def test_basic(executor):
    test_repo_dir = executor.run(
        TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images"
    )
    assert_files_equal(test_repo_dir, TEST_DATA_SAMPLE_DIR / "basic")
    assert assert_weedcoco_equal(test_repo_dir, TEST_DATA_SAMPLE_DIR / "basic")


def test_duplicate_images(executor):
    with pytest.raises(
        ValidationError, match="There are identical images in the image directory."
    ):
        executor.run(
            TEST_DUPLICATE_DIR / "weedcoco.json", TEST_DUPLICATE_DIR / "images"
        )


def test_existing_images(executor):
    with pytest.raises(
        ValidationError, match="There are identical images in the repository."
    ):
        executor.run(TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images")
        executor.run(TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images")


def test_multiple_collections(executor):
    executor.run(TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images")
    test_repo_dir = executor.run(
        TEST_BASIC_DIR_2 / "weedcoco.json", TEST_BASIC_DIR_2 / "images"
    )
    assert_files_equal(test_repo_dir, TEST_DATA_SAMPLE_DIR / "multiple")
    assert assert_weedcoco_equal(test_repo_dir, TEST_DATA_SAMPLE_DIR / "multiple")
