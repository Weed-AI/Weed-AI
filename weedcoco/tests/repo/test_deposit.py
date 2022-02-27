import pathlib
import json
import pytest
import os
import filecmp
import re
import subprocess
import shutil
from weedcoco.repo.deposit import main, RepositoryDataset, mkdir_safely
from weedcoco.validation import ValidationError

TEST_DATA_DIR = pathlib.Path(__file__).parent / "deposit_data"
TEST_DATA_SAMPLE_DIR = pathlib.Path(__file__).parent / "deposit_data_sample"
TEST_BASIC_DIR_1 = TEST_DATA_DIR / "basic_1"
TEST_BASIC_DIR_2 = TEST_DATA_DIR / "basic_2"
TEST_COMPLETE_DIR = TEST_DATA_DIR / "complete"
TEST_DUPLICATE_DIR = TEST_DATA_DIR / "duplicate"

TEST_NAME = "weed.ai"
TEST_ADDRESS = "weed@weed.ai.org"
TEST_MESSAGE = "Test commit"


@pytest.fixture
def executor(tmpdir):
    test_repo_dir = tmpdir / "test_repo"
    test_download_dir = tmpdir / "test_download"
    test_extract_dir = tmpdir / "test_extract"
    mkdir_safely(test_extract_dir)

    class Executor:
        def run(
            self,
            identifier,
            weedcoco_path,
            image_dir,
            repository_dir=test_repo_dir,
            download_dir=test_download_dir,
            name=TEST_NAME,
            address=TEST_ADDRESS,
            message=TEST_MESSAGE,
        ):
            args = [
                "--identifier",
                identifier,
                "--weedcoco-path",
                weedcoco_path,
                "--image-dir",
                image_dir,
                "--repository-dir",
                repository_dir,
                "--download-dir",
                download_dir,
                "--name",
                name,
                "--address",
                address,
                "--message",
                message,
            ]
            args = [str(arg) for arg in args]
            repo, dataset = main(args)
            return test_extract_dir, repo, dataset

    return Executor()


def assert_files_equal(dir1, dir2):
    dirs_cmp = filecmp.dircmp(dir1, dir2, ignore=[".DS_Store"])
    assert len(dirs_cmp.left_only) == 0
    assert len(dirs_cmp.right_only) == 0
    assert len(dirs_cmp.funny_files) == 0
    match, mismatch, errors = filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False
    )
    for filename in mismatch:
        print(f"Differences in {filename}")
        subprocess.run(["diff", f"{dir1}/{filename}", f"{dir2}/{filename}"])
        print("Is rerunning pytest with --rewrite-deposit-truth appropriate?")
    assert len(mismatch) == 0
    assert len(errors) == 0
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        assert_files_equal(new_dir1, new_dir2)


def assert_weedcoco_equal(dir1, dir2):
    for dir in os.listdir(dir2):
        if re.fullmatch(r"^dataset_\d+$", dir):
            assert json.load(open(dir1 / dir / "weedcoco.json")) == json.load(
                open(dir2 / dir / "weedcoco.json")
            )


def rewrite_outputs(repo, expected_dir):
    """Copies the content in test_repo to the fixtures directory.

    Has to be a bit more complicated with an ocfl repo

    TODO - hasn't been tested!
    """
    shutil.rmtree(expected_dir)
    mkdir_safely(expected_dir)
    repo.connnect()
    for path in repo.object_paths():
        obj_id = path.replace("/", "")
        obj = RepositoryDataset(repo, obj_id)
        obj.extract(str(expected_dir / pathlib.Path(obj_id)))
    # shutil.copytree(actual_dir, expected_dir, symlinks=True) # symlinks? maybe fixme


def test_basic(executor, rewrite_deposit_truth):
    test_extract_dir, repo, dataset = executor.run(
        "dataset_1", TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images"
    )

    if rewrite_deposit_truth:
        rewrite_outputs(repo, TEST_DATA_SAMPLE_DIR / "basic")
    dataset.extract(str(test_extract_dir / pathlib.Path("dataset_1")))
    assert_files_equal(test_extract_dir, TEST_DATA_SAMPLE_DIR / "basic")
    assert_weedcoco_equal(test_extract_dir, TEST_DATA_SAMPLE_DIR / "basic")


def test_duplicate_images(executor):
    with pytest.raises(
        ValidationError,
        match="There are identical images in the image directory. Identical image sets are: 001_image.png <-> 002_image.png",
    ):
        executor.run(
            "dataset1",
            TEST_DUPLICATE_DIR / "weedcoco.json",
            TEST_DUPLICATE_DIR / "images",
        )


def test_existing_images(executor):
    with pytest.raises(
        ValidationError, match="There are identical images in the repository."
    ):
        executor.run(
            "dataset1", TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images"
        )
        executor.run(
            "dataset2", TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images"
        )


def test_multiple_datasets(executor, rewrite_deposit_truth):
    test_extract_dir, repo, dataset1 = executor.run(
        "dataset_1", TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images"
    )
    _, _, dataset2 = executor.run(
        "dataset_2", TEST_BASIC_DIR_2 / "weedcoco.json", TEST_BASIC_DIR_2 / "images"
    )
    if rewrite_deposit_truth:
        rewrite_outputs(repo, TEST_DATA_SAMPLE_DIR / "multiple")
    dataset1.extract(str(test_extract_dir / pathlib.Path("dataset_1")))
    dataset2.extract(str(test_extract_dir / pathlib.Path("dataset_2")))
    assert_files_equal(test_extract_dir, TEST_DATA_SAMPLE_DIR / "multiple")
    assert_weedcoco_equal(test_extract_dir, TEST_DATA_SAMPLE_DIR / "multiple")
