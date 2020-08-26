TARGETS=$(patsubst %.yaml, %.json, $(wildcard *.yaml))

all: $(TARGETS)


%.json: %.yaml
	python -c 'import json, yaml, sys; json.dump(yaml.safe_load(sys.stdin), sys.stdout, indent=2)' < $< > $@
