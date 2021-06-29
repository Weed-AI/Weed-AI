#!/bin/bash
set -ex

# To be run in repository dir

usage() {
	echo "Usage:  $0 <git_remote> <dvc_remote> <commit_msg>" >&1
	exit 1
}

if [ -z "$1" -o -n "$4" ]
then
    usage
fi

git_remote="$1"
dvc_remote="$2"
commit_msg="$3"

if [ ! -x .git ]
then
    git init
fi
if [ ! -x .dvc ]
then
    dvc init
    git commit -m "Initialise DVC"
fi

git remote remove storage || true
git remote add storage "$git_remote"
dvc remote add -f -d storage "$dvc_remote"

dvc add */images
git add */*.json
dvc commit
git add */images.dvc
git commit -m "$commit_msg" || (echo "Nothing to commit"; exit 0)
dvc push
git push storage master:master

