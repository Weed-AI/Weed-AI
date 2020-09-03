#! zsh

mypath=$0:A
conversion_root=$(dirname "$mypath")/../../conversion_tools

conv() {
    python "$conversion_root"'/draft export to elastic.py' "$@"
}

(
	conv --thumbnail-dir deepweeds  < $conversion_root/deepweeds_to_json/deepweeds_imageinfo.json
	conv --thumbnail-dir cwfid  < $conversion_root/cwfid_to_json/cwfid_imageinfo.json
) |
	curl -X POST localhost:9200/_bulk  -H 'Content-Type: application/json' --data-binary @-
