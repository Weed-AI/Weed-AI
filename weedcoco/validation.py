import pathlib

SCHEMA_DIR = pathlib.Path(__file__).parent / "schema"


def validate_json(weedcoco, schema_dir=SCHEMA_DIR):
    """Check that the weedcoco matches its JSON schema"""
    # TODO


def validate_references(weedcoco, schema_dir=SCHEMA_DIR):
    """Check that all IDs are valid references"""
    # TODO


def validate_coordinates(weedcoco):
    """Check that annotation coordinates are within the image"""
    # TODO


def validate_image_sizes(weedcoco, images_root):
    """Check that all image sizes match the image files"""
    # TODO


def validate(weedcoco, images_root=None):
    validate_json(weedcoco)
    validate_references(weedcoco)
    validate_coordinates(weedcoco)
    if images_root is not None:
        validate_image_sizes(weedcoco, images_root)
