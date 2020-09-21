"""Tests for weedcoco.validation"""

import functools

import pytest
import jsonschema

from weedcoco.validation import (
    validate,
    validate_json,
    validate_references,
    validate_coordinates,
    validate_image_sizes,
    ValidationError,
)

validate_image_sizes_null = functools.partial(validate_image_sizes, images_root=None)
validate_image_sizes_cwd = functools.partial(validate_image_sizes, images_root=".")


MINIMAL_WEEDCOCO = {
    "images": [],
    "annotations": [],
    "categories": [],
    "agcontexts": [],
    "collections": [],
    "collection_memberships": [],
    "info": {},
}
# TODO: NON_TRIVIAL_WEEDCOCO


@pytest.mark.parametrize("func", [validate, validate_json])
@pytest.mark.parametrize(
    "bad_weedcoco",
    [
        {},
        {"images": [], "annotations": []},
        {"images": [], "annotations": [], "categories": []},
    ],
)
def test_missing_required_at_root(func, bad_weedcoco):
    with pytest.raises(jsonschema.ValidationError, match="is a required property"):
        func(bad_weedcoco)


@pytest.mark.parametrize(
    "func",
    [
        validate,
        validate_json,
        validate_references,
        validate_coordinates,
        validate_image_sizes_null,
        validate_image_sizes_cwd,
    ],
)
def test_minimal(func):
    func(MINIMAL_WEEDCOCO)


@pytest.mark.parametrize("func", [validate, validate_json])
@pytest.mark.parametrize("bad_weedcoco", [])  # TODO
def test_duplicate_id(func, bad_weedcoco):
    with pytest.raises(ValidationError, match="Duplicate ID"):
        func(bad_weedcoco)


@pytest.mark.parametrize("func", [validate, validate_json])
@pytest.mark.parametrize("bad_weedcoco", [])  # TODO
def test_nonexistent_referent(func, bad_weedcoco):
    with pytest.raises(ValidationError, match="Reference to unknown ID"):
        func(bad_weedcoco)


@pytest.mark.parametrize("func", [validate, validate_json])
@pytest.mark.parametrize("bad_weedcoco", [])  # TODO
def test_id_not_referenced(func, bad_weedcoco):
    with pytest.raises(ValidationError, match="Not all objects are referenced"):
        func(bad_weedcoco)
