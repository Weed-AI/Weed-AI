import numpy as np
import imagehash
import argparse
import pathlib
import os
import scipy.spatial
import PIL.Image
import seaborn as sns
import matplotlib.pyplot as plt
from weedcoco.utils import check_if_approved_image_format


sns.set_theme(color_codes=True)

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument("--dataset-dir", required=True, type=pathlib.Path)
args = ap.parse_args()

X = np.asarray(
    [
        imagehash.average_hash(
            PIL.Image.open(f"{dirpath}/{filename}"), hash_size=16
        ).hash.flatten()
        for dirpath, dirnames, filenames in os.walk(args.dataset_dir)
        if os.path.basename(dirpath) == "img"
        for filename in filenames
        if check_if_approved_image_format(filename)
    ]
)
distances = scipy.spatial.distance.pdist(X, metric="hamming")
g = sns.displot(distances)
plt.show()
