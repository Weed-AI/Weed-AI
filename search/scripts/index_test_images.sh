#! zsh

mypath=$0:A
repo_root=$(dirname "$mypath")/../../

if [ -n "$1" ]
then
	elastic_host="$1"
fi

conv() {
    python "$repo_root"'/search/scripts/weedcoco-to-elastic-index-bulk.py' "$@"
}

(
	conv --thumbnail-dir deepweeds  < $repo_root/weedcoco/deepweeds_to_json/deepweeds_imageinfo.json
	conv --thumbnail-dir cwfid  < $repo_root/weedcoco/cwfid_to_json/cwfid_imageinfo.json
) |
	curl -X POST $elastic_host/_bulk  -H 'Content-Type: application/json' --data-binary @-
