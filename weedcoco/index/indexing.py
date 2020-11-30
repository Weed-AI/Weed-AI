import argparse
import os
import pathlib
import json
from elasticsearch import Elasticsearch, helpers


class ElasticSearchIndex:

    """
    Args:
        weedcoco_path (pathlib.PosixPath): weedcoco local path for indexing
        thumbnail_dir (pathlib.PosixPath): thumbnail folder local path to be integrated into the json file for indexing
        es_index_name (string): index name for ElasticSearch
        es_type_name (string): type name for ElasticSearch
        batch_size (int): split json file for indexing into batches to reduce the payload of each request
        es_host (string): ElasticSearch server host to send request
        es_port (int): ElasticSearch server port to send request
        indexes (dict): base file to build index json file
    """

    def __init__(
        self,
        weedcoco_path,
        thumbnail_dir,
        es_index_name="weedid",
        es_type_name="image",
        batch_size=30,
        es_host="http://localhost",
        es_port=9200,
        indexes=None,
    ):
        self.weedcoco_path = weedcoco_path
        self.thumbnail_dir = thumbnail_dir
        self.es_index_name = es_index_name
        self.es_type_name = es_type_name
        self.batch_size = batch_size
        self.es_client = Elasticsearch(HOST=es_host, PORT=es_port)
        self.indexes = indexes if indexes is not None else {}

    def modify_coco(self):
        """
        Create index entries for request to ElasticSearch
        """

        def _flatten(src, dst, prefix):
            for k, v in src.items():
                dst[f"{prefix}__{k}"] = v

        with open(self.weedcoco_path) as f:
            coco = json.load(f)
        if "info" in coco:
            del coco["info"]
        if "collection_memberships" in coco:
            del coco["collection_memberships"]

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
                self.thumbnail_dir
                / os.path.basename(image["file_name"])[:2]
                / os.path.basename(image["file_name"])
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

        self.indexes = coco

    def generate_batches(self):
        """
        Split indexes into batches to reduce payload size of each request to ElasticSearch
        """
        indexes = self.indexes
        if "images" in indexes and len(indexes["images"]) > 0:
            images = indexes["images"]
            for start in range(0, len(images), self.batch_size):
                blobs = []
                batch = images[start : start + self.batch_size]
                for image in batch:
                    blobs.append(
                        {
                            "_index": self.es_index_name,
                            "_type": self.es_type_name,
                            "_source": image,
                        }
                    )
                yield blobs

    def post_to_index(self):
        """
        Send post request to ElasticSearch
        """
        for index_batch in self.generate_batches():
            helpers.bulk(self.es_client, index_batch)


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--weedcoco-path", type=pathlib.Path, required=True)
    ap.add_argument("--thumbnail-dir", type=pathlib.Path, required=True)
    args = ap.parse_args(args)
    return ElasticSearchIndex(args.weedcoco_path, args.thumbnail_dir)


if __name__ == "__main__":
    es_index = main()
    es_index.modify_coco()
    es_index.post_to_index()
