#! zsh

mypath=$0:A
conversion_root=$(dirname "$mypath")/../../conversion_tools

for json_path in $conversion_root/deepweeds_to_json/deepweeds_imageinfo.json $conversion_root/cwfid_to_json/cwfid_imageinfo.json
do
	python "$conversion_root"'/draft export to elastic.py'  < $json_path |
		curl -X POST localhost:9200/_bulk  -H 'Content-Type: application/json' --data-binary @-
done
