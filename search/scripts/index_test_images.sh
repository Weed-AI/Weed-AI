#! zsh

mypath=$0:A
repo_root=$(dirname "$mypath")/../../

conv() {
    python "$repo_root"'/search/scripts/weedcoco_to_elastic_index_bulk.py' "$@"
}

(
	conv --thumbnail-dir deepweeds  < $repo_root/weedcoco/deepweeds_to_json/deepweeds_imageinfo.json
	conv --thumbnail-dir cwfid  < $repo_root/weedcoco/cwfid_to_json/cwfid_imageinfo.json
) |
	curl -X POST localhost:9200/_bulk  -H 'Content-Type: application/json' --data-binary @-
