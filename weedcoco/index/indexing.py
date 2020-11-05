import argparse
import os
import pathlib
import json
import requests
from math import ceil


class ElasticSearchIndex:
    def __init__(
        self,
        weedcoco_path,
        thumbnail_dir,
        temp_index_dir="temp",
        index_batch=30,
        es_url="http://localhost:9200/",
        coco={},
    ):
        self.weedcoco_path = weedcoco_path
        self.thumbnail_dir = thumbnail_dir
        self.temp_index_dir = temp_index_dir
        self.index_batch = index_batch
        self.es_url = es_url
        self.coco = coco

        if (
            self.temp_index_dir == "temp"
            or not os.path.isdir(self.temp_index_dir)
            and "temp" not in os.listdir()
        ):
            self.temp_index_dir = "temp"
            os.mkdir(self.temp_index_dir)

    def modify_coco(self):
        def _flatten(src, dst, prefix):
            for k, v in src.items():
                dst[f"{prefix}__{k}"] = v

        with open(self.weedcoco_path) as f:
            coco = json.load(f)
        try:
            del coco["info"]
            del coco["collection_memberships"]
        except KeyError:
            pass

        id_lookup = {}
        for key, objs in coco.items():
            for obj in objs:
                id_lookup[key, obj["id"]] = obj

        variable_to_null_fields = ["camera_fov", "camera_lens_focallength"]

        for agcontext in coco["agcontexts"]:
            # massage for ES
            for field in variable_to_null_fields:
                if agcontext.get(field) == "variable":
                    del agcontext[field]

        for annotation in coco["annotations"]:
            image = id_lookup["images", annotation["image_id"]]
            image.setdefault("annotations", []).append(annotation)
            annotation["category"] = id_lookup["categories", annotation["category_id"]]
            # todo: add collection, license
            _flatten(annotation["category"], annotation, "category")
            # todo: add collection from collection_memberships
            image["thumbnail"] = str(
                self.thumbnail_dir / os.path.basename(image["file_name"])
            )

        for image in coco["images"]:
            try:
                image["resolution"] = image["width"] * image["height"]
            except KeyError:
                pass
            image["agcontext"] = id_lookup["agcontexts", image["agcontext_id"]]
            image["sortKey"] = hash(
                image["file_name"]
            )  # for deterministic random order
            _flatten(image["agcontext"], image, "agcontext")
            # todo: add license
            image["task_type"] = set()
            for annotation in image["annotations"]:
                for k in annotation:
                    image.setdefault(f"annotation__{k}", []).append(annotation[k])

                # determine available task types
                image["task_type"].add("classification")
                if "segmentation" in annotation:
                    image["task_type"].add("segmentation")
                    image["task_type"].add("bounding box")
                if "bbox" in annotation:
                    image["task_type"].add("bounding box")
            image["task_type"] = sorted(image["task_type"])

        self.coco = coco

    def generate_batches(self):

        coco = self.coco
        if "images" in coco and len(coco["images"]) > 0:
            for i in range(ceil(len(coco["images"]) / self.index_batch)):
                with open(f"{self.temp_index_dir}/index{str(i+1)}.json", "w") as f:
                    for image in coco["images"][
                        i
                        * self.index_batch : min(
                            len(coco["images"]), (i + 1) * self.index_batch
                        )
                    ]:
                        json.dump({"index": {"_index": "weedid", "_type": "image"}}, f)
                        f.write("\n")
                        json.dump(image, f)
                        f.write("\n")

    def post_index(self):

        files = [
            file for file in os.listdir(self.temp_index_dir) if file.endswith(".json")
        ]
        for item in files:
            requests.post(
                f"{self.es_url}_bulk",
                data=open(f"{self.temp_index_dir}/{item}", "rb").read(),
                headers={"content-type": "application/json"},
            )


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--weedcoco-path", type=pathlib.Path, required=True)
    ap.add_argument("--thumbnail-dir", type=pathlib.Path, required=True)
    args = ap.parse_args(args)
    return ElasticSearchIndex(args.weedcoco_path, args.thumbnail_dir)


if __name__ == "__main__":
    es_index = main()
    es_index.modify_coco()
    es_index.generate_batches()
    es_index.post_index()
