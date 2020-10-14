#! zsh
# Clean refresh of ES data and thumbnails given path to RDS
# For use by the project team at the University of Sydney

# TODO: make elastic index name configurable and/or use index aliases to make the change atomic
# TODO: handle demo mode, e.g. to export random 10 images from each dataset

set -ex

mypath=$0:A
repo_root=$(dirname "$mypath")/../../

usage() {
	echo $0 "[-r /path/to/rds] [-H http://elastic:9200] [OPTIONS]" >&2
	echo Options: >&2
	echo " -r|--rds      Set the path to the iweeds RDS" >&2
	echo " -H|--host     Specify the elastic host and port" >&2
	echo " --no-purge    Do not purge the existing index on elastic" >&2
	echo " --no-thumbs   Do not copy thumbnails into the static file server" >&2
	echo " --demo        Only index a small sample for demonstration" >&2
	exit 1
}

if [ -d /Volumes/research-data/PRJ-iweeds ]
then
	rds_root=/Volumes/research-data/PRJ-iweeds 
else
	rds_root=/rds/PRJ-iweeds
fi

elastic_host=http://localhost:9200
get_thumbs=1
demo_mode=0

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--help) usage ;;
        -r|--rds) rds_root="$2"; shift ;;
        -H|--host) elastic_host="$2"; shift ;;
		--no-thumbs) get_thumbs=0; shift ;;
		--demo) demo_mode=1; shift ;;
        *) echo "Unknown parameter passed: $1"; usage ;;
    esac
    shift
done

if [ $get_thumbs == 1 ]
then
	rm -r $repo_root/search/public/thumbnails/*
	$repo_root/search/scripts/download_test_thumbnails.sh
fi

scripts/index_test_images.sh


dir=$rds_root/data/raw/SOLES/narrabri/2019-winter/20190728
python -m weedcoco.importers.voc --voc-dir $dir/voc --image-dir $dir/img --category-name-map $dir/category-name-map.yaml --collection $dir/collection.yaml --agcontext $dir/agcontext.yaml -o /tmp/coco_from_voc-test.json
cat /tmp/coco_from_voc-test.json | python $repo_root/search/scripts/weedcoco-to-elastic-index-bulk.py --thumbnail-dir artificial | curl -vv -X POST $elastic_host/_bulk  -H 'Content-Type: application/json' --data-binary @-

