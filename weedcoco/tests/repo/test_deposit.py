import filecmp
import json
import os
import pathlib
import re
import shutil
import subprocess
import zipfile

import pytest
from weedcoco.index.thumbnailing import thumbnailing
from weedcoco.repo.deposit import main, mkdir_safely
from weedcoco.validation import ValidationError

TEST_DATA_DIR = pathlib.Path(__file__).parent / "deposit_data"
TEST_DATA_SAMPLE_DIR = pathlib.Path(__file__).parent / "deposit_data_sample"
TEST_BASIC_DIR_1 = TEST_DATA_DIR / "basic_1"
TEST_BASIC_DIR_1V2 = TEST_DATA_DIR / "basic_1.v2"
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
    mkdir_safely(test_download_dir)

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
            return test_extract_dir, test_download_dir, repo, dataset

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


def unpack_zip(zip_path, destination):
    z = zipfile.ZipFile(zip_path)
    z.extractall(str(destination))


def rewrite_outputs(repo, expected_dir, versions=False):
    """Copies the content in repo to the fixtures directory. Used to regenerate
    content in deposit_data_sample.

    repo - the ocfl repository
    expected_dir - the directory within deposit_data_sample
    versions - if true, extracts each version of the datasets into directories
    with names like expected_dir/identifier.v1, expected_dir/identifier.v2 etc

    Default behaviour is to just extract the head version
    """
    shutil.rmtree(expected_dir)
    mkdir_safely(expected_dir)
    for dataset in repo.datasets():
        identifier = dataset.identifier
        if versions:
            head = int(dataset.head_version[1:])
            for version_number in range(1, head + 1):
                d = str(expected_dir / pathlib.Path(identifier)) + f".v{version_number}"
                dataset.extract(d, f"v{version_number}")
        else:
            dataset.extract(str(expected_dir / pathlib.Path(identifier)))


def test_basic(executor, rewrite_deposit_truth):
    test_extract_dir, _, repo, dataset = executor.run(
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


def test_existing_no_self_match(executor):
    executor.run(
        "dataset1", TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images"
    )
    executor.run(
        "dataset1", TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images"
    )


def test_multiple_datasets(executor, rewrite_deposit_truth):
    test_extract_dir, _, repo, dataset1 = executor.run(
        "dataset_1", TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images"
    )
    _, _, _, dataset2 = executor.run(
        "dataset_2", TEST_BASIC_DIR_2 / "weedcoco.json", TEST_BASIC_DIR_2 / "images"
    )
    if rewrite_deposit_truth:
        rewrite_outputs(repo, TEST_DATA_SAMPLE_DIR / "multiple")
    dataset1.extract(str(test_extract_dir / pathlib.Path("dataset_1")))
    dataset2.extract(str(test_extract_dir / pathlib.Path("dataset_2")))
    assert_files_equal(test_extract_dir, TEST_DATA_SAMPLE_DIR / "multiple")
    assert_weedcoco_equal(test_extract_dir, TEST_DATA_SAMPLE_DIR / "multiple")


def test_versioned_datasets(executor, rewrite_deposit_truth):
    test_extract_dir, test_download_dir, repo, _ = executor.run(
        "dataset_1", TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images"
    )
    test_extract_dir, _, repo, _ = executor.run(
        "dataset_1", TEST_BASIC_DIR_1V2 / "weedcoco.json", TEST_BASIC_DIR_1V2 / "images"
    )
    dataset = repo.dataset("dataset_1")
    assert dataset.head_version == "v2"
    if rewrite_deposit_truth:
        rewrite_outputs(repo, TEST_DATA_SAMPLE_DIR / "versions", True)
    dataset.extract(str(test_extract_dir / "dataset_1.v1"), "v1")
    dataset.extract(str(test_extract_dir / "dataset_1.v2"), "v2")
    assert_files_equal(test_extract_dir, TEST_DATA_SAMPLE_DIR / "versions")
    assert_weedcoco_equal(test_extract_dir, TEST_DATA_SAMPLE_DIR / "versions")
    mkdir_safely(str(test_extract_dir / "zipfiles"))
    unpack_zip(
        test_download_dir / "dataset_1.v1.zip",
        test_extract_dir / "zipfiles" / "dataset_1.v1",
    )
    unpack_zip(
        test_download_dir / "dataset_1.zip",
        test_extract_dir / "zipfiles" / "dataset_1.v2",
    )
    assert_weedcoco_equal(
        test_extract_dir / "zipfiles", TEST_DATA_SAMPLE_DIR / "versions"
    )


def test_thumbnails(executor):
    test_extract_dir, _, repo, dataset1 = executor.run(
        "dataset_1", TEST_BASIC_DIR_1 / "weedcoco.json", TEST_BASIC_DIR_1 / "images"
    )
    # temp dirs are LocalPaths, cast to Path so we can use is_file
    test_extract_dir = pathlib.Path(test_extract_dir)
    # make thumbnails in the extract dir
    thumbnailing(test_extract_dir, repo.root, "dataset_1")
    images = [
        path.split("/")[1]
        for path in dataset1.get_logical_paths()
        if path.split("/")[0] == "images"
    ]
    for image in images:
        thumbnail = test_extract_dir / image[:2] / image
        bbox = test_extract_dir / ("bbox-" + image[:2]) / image
        assert thumbnail.is_file()
        assert bbox.is_file()
