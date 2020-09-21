import PIL.Image
import os
import warnings


def get_image_dimensions(path):
    """
    Function to measure image dimensions and calculate resolution.
    """
    if not os.path.isfile(path):
        warnings.warn(f"Could not open {path}")
        return None
    # Retrieve image width and height
    image = PIL.Image.open(path)
    width, height = image.size
    # Calculate resolution in pixels
    resolution = width * height
    return {"width": width, "height": height, "resolution": resolution}
