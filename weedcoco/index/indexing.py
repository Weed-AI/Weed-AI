import argparse
import json
import os
import pathlib
import sys
from uuid import uuid4

import elasticsearch  # using `from elastisearch` breaks elasticmock
from elasticsearch import helpers
from weedcoco.utils import (
    denormalise_weedcoco,
    get_supercategory_names,
    get_task_types,
    lookup_growth_stage_name,
)


class ElasticSearchIndexer:

    """
    Args:
        weedcoco_path (pathlib.PosixPath): weedcoco local path for indexing
        thumbnail_dir (pathlib.PosixPath): thumbnail folder local path to be integrated into the json file for indexing
        es_index_name (string): index name for ElasticSearch
        batch_size (int): split json file for indexing into batches to reduce the payload of each request
        es_host (string): ElasticSearch server host to send request
        es_port (int): ElasticSearch server port to send request
        indexes (dict): base file to build index json file
        dry_run (bool): when True, ignore elastic server and print to stdout
    """

    def __init__(
        self,
        weedcoco_path,
        thumbnail_dir,
        es_index_name="weedid",
        batch_size=30,
        es_host="localhost",
        es_port=9200,
        indexes=None,
        upload_id="#",
        version_id=str(uuid4()),
        dry_run=False,
    ):
        self.weedcoco_path = pathlib.Path(weedcoco_path)
        self.thumbnail_dir = pathlib.Path(thumbnail_dir)
        self.es_index_name = es_index_name
        self.batch_size = batch_size
        self.dry_run = dry_run
        hosts = [{"host": es_host, "port": es_port}]
        if dry_run:
            self.es_client = sys.stdout
        else:
            self.es_client = elasticsearch.Elasticsearch(hosts=hosts)
        self.indexes = indexes if indexes is not None else {}
        self.upload_id = upload_id
        self.version_id = version_id

    def generate_index_entries(self):
        """
        Create index entries for request to ElasticSearch
        """

        def _flatten(src, dst, prefix):
            for k, v in src.items():
                dst[f"{prefix}__{k}"] = v

        with open(self.weedcoco_path) as f:
            coco = json.load(f)

        denormalise_weedcoco(coco)

        variable_to_null_fields = ["camera_fov", "camera_lens_focallength"]
        na_to_null_fields = ["bbch_growth_range"]

        for category in coco["categories"]:
            category["taxo_names"] = [category["name"]] + get_supercategory_names(
                category["name"]
            )

        for agcontext in coco["agcontexts"]:
            # massage for ES
            for field in variable_to_null_fields:
                if agcontext.get(field) == "variable":
                    del agcontext[field]
            for field in na_to_null_fields:
                if agcontext.get(field) == "na":
                    del agcontext[field]
            # textual label for growth stage
            if "bbch_growth_range" not in agcontext:
                growth_stage_texts = ["na"]
            else:
                lo = agcontext["bbch_growth_range"]["min"]
                hi = agcontext["bbch_growth_range"]["max"]
                growth_stage_texts = set()
                for i in range(lo, hi + 1):
                    growth_stage_texts.add(
                        lookup_growth_stage_name(i, scheme="grain_ranges")
                    )
                agcontext["growth_stage_min_text"] = lookup_growth_stage_name(
                    lo, scheme="grain_ranges"
                )
                agcontext["growth_stage_max_text"] = lookup_growth_stage_name(
                    hi, scheme="grain_ranges"
                )
            agcontext["growth_stage_texts"] = sorted(growth_stage_texts)

        for annotation in coco["annotations"]:
            _flatten(annotation["category"], annotation, "category")

        for image in coco["images"]:
            # todo: add data from info, license?

            image["thumbnail"] = str(
                self.thumbnail_dir
                / os.path.basename(image["file_name"])[:2]
                / os.path.basename(image["file_name"])
            )
            image["thumbnail_bbox"] = str(
                self.thumbnail_dir
                / ("bbox-" + os.path.basename(image["file_name"])[:2])
                / os.path.basename(image["file_name"])
            )
            image["upload_id"] = f"{self.upload_id}"

            try:
                image["resolution"] = image["width"] * image["height"]
            except KeyError:
                pass
            image["sortKey"] = hash(
                image["file_name"]
            )  # for deterministic random order
            _flatten(image["agcontext"], image, "agcontext")
            # todo: add license
            if "annotations" not in image:
                image["annotations"] = list()
            for annotation in image["annotations"]:
                for k in annotation:
                    image.setdefault(f"annotation__{k}", []).append(annotation[k])

            image["task_type"] = sorted(get_task_types(image["annotations"]))
            image[
                "location"
            ] = f'{image["agcontext"]["location_lat"]}, {image["agcontext"]["location_long"]}'
            image["dataset_name"] = coco["info"]["metadata"]["name"]
            image["version"] = {
                "version_id": self.version_id,
                "version_tag": "latest version",
            }
            yield image

    def generate_batches(self):
        """
        Split indexes into batches to reduce payload size of each request to ElasticSearch
        """
        images = list(self.generate_index_entries())
        for start in range(0, len(images), self.batch_size):
            blobs = []
            batch = images[start : start + self.batch_size]
            for image in batch:
                blobs.append(
                    {
                        "_index": self.es_index_name,
                        "_id": os.path.basename(image["file_name"]),
                        "_source": image,
                    }
                )
            yield blobs

    def post_index_entries(self):
        """
        Send post request to ElasticSearch
        """
        for index_batch in self.generate_batches():
            if hasattr(self.es_client, "bulk"):
                helpers.bulk(self.es_client, index_batch)
            else:
                # a file for dry run
                self.es_client.write(json.dumps(index_batch, indent=2))
        if not self.dry_run:
            self.archive_other_versions()

    def archive_other_versions(self):
        # in case other filenames had been submitted with this upload_id
        if self.upload_id == "#":
            raise ValueError("archive_other_versions requires upload_id != '#'")
        assert '"' not in self.upload_id
        assert "\\" not in self.upload_id

        if not hasattr(self.es_client, "bulk"):
            return
        body = f"""
        {{
          "script": {{
            "source": "ctx._source.version.version_tag = 'past version'"
          }},
          "query": {{
            "bool": {{
              "must": {{"match": {{"upload_id": "{self.upload_id}"}}}},
              "must_not": {{"match": {{"version.version_id": "{self.version_id}"}}}}
            }}
          }}
        }}
        """
        self.es_client.update_by_query(self.es_index_name, body, conflicts="proceed")

    @staticmethod
    def remove_all_index_with_upload(
        upload_id, es_index_name="weedid", es_host="localhost", es_port=9200
    ):
        es_client = elasticsearch.Elasticsearch(
            hosts=[{"host": es_host, "port": es_port}]
        )
        body = f"""
        {{
          "script": {{
            "source": "ctx._source.version.version_tag = 'past version'"
          }},
          "query": {{
            "bool": {{
              "must": {{"match": {{"upload_id": "{upload_id}"}}}}
            }}
          }}
        }}
        """
        es_client.update_by_query(es_index_name, body, conflicts="proceed")


def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--weedcoco-path", type=pathlib.Path, required=True)
    ap.add_argument("--thumbnail-dir", type=pathlib.Path, required=True)
    ap.add_argument("--upload-id", required=True)
    ap.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="When set, index entries will be printed to stdout instead of the Elastic server.",
    )
    args = ap.parse_args(args)
    ElasticSearchIndexer(
        args.weedcoco_path,
        args.thumbnail_dir,
        dry_run=args.dry_run,
        upload_id=args.upload_id,
    ).post_index_entries()


if __name__ == "__main__":
    main()
