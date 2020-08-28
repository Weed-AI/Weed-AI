import yaml
import textwrap
schema = yaml.safe_load(open('AgContext.yaml'))
required = schema['required']
for name, prop in schema['properties'].items():
    prop['required'] = name in required
    print(f"### {name} ###")
    print(textwrap.indent(yaml.dump(prop), '# '))
    print(f"{name}: <TO DO: insert value here{' or remove this line' if name not in required else ''}>")
    print()
