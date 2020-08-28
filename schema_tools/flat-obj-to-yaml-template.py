"""Turn a schema for a flat JSON object into a YAML template for completion
"""
import yaml
import json
import textwrap
import argparse

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('schema_path')
args = ap.parse_args()

if args.schema_path.endswith(('.yaml', '.yml')):
    schema = yaml.safe_load(open(args.schema_path))
else:
    schema = json.load(open(args.schema_path))

required = schema['required']
for name, prop in schema['properties'].items():
    prop['required'] = name in required
    print(f"### {name} ###")
    print(textwrap.indent(yaml.dump(prop), '# '))
    print(f"{name}: <TO DO: insert value here{' or remove this line' if name not in required else ''}>")
    print()
