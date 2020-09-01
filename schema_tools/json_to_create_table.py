#!/usr/bin/env python
"""Convert COCO-like JSON to PostgreSQL CREATE TABLE statements
"""

import argparse
import json
from collections import Counter, defaultdict


def pluralise(k):
    if k.endswith("y"):
        return f"{k[:-1]}ies"
    if k.endswith("data"):
        return k
    return f"{k}s"


def convert_json_to_create_table(json_paths):
    types = defaultdict(dict)
    counts = defaultdict(Counter)
    n_objects = 0
    for json_path in json_paths:
        with open(json_path) as f:
            blob = json.load(f)

        for table_name, table_data in blob.items():
            if table_name == "info":
                # TODO: handle later?
                continue
            table_types = types[table_name]
            table_counts = counts[table_name]

            n_objects += len(table_data)
            for obj in table_data:
                if not hasattr(obj, "items"):
                    print(obj)
                for k, v in obj.items():
                    table_counts[k] += 1
                    typ_name = type(v).__name__
                    if k in table_types:
                        assert table_types[k] == typ_name
                    table_types[k] = typ_name

    out = ""
    for table_name, table_types in types.items():
        table_counts = counts[table_name]

        out += f"CREATE TABLE {table_name} (\n"
        clauses = [
            f"{k} {typ}{' NULL' if table_counts[k] < n_objects else ''}"
            for k, typ in table_types.items()
        ]
        if "id" in table_types:
            clauses.append("PRIMARY KEY (id)")
        for k in table_types:
            if k[-3:] == "_id":
                clauses.append(
                    f"FOREIGN KEY ({k}) " f"REFERENCES {pluralise(k[:-3])} (id)"
                )
        out += "    " + ",\n    ".join(clauses) + "\n"
        out += f");\n"
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("json_paths", nargs="+")
    args = ap.parse_args()
    print(convert_json_to_create_table(args.json_paths))
