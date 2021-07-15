#!/usr/bin/env zsh

mypath=$0:A
repo_root=$(dirname "$mypath")/../../

usage() {
	echo $0 "[OPTIONS]" >&2
	echo Options: >&2
#	echo " -r|--rds      Set the path to the iweeds RDS" >&2
#	echo " -H|--host     Specify the elastic host and port" >&2
	exit 1
}

elastic_host=http://localhost:9200

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) usage ;;
#        -r|--rds) rds_root="$2"; shift ;;
#        -H|--host) elastic_host="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done


post() {
    python -m weedcoco.index.indexing "$@"
}

(
	post --thumbnail-dir deepweeds --weedcoco-path "$repo_root/weedcoco/deepweeds_to_json/deepweeds_imageinfo.json" --upload-id deepweeds
	post --thumbnail-dir cwfid --weedcoco-path "$repo_root/weedcoco/cwfid_to_json/cwfid_imageinfo.json" --upload cwfid
)
