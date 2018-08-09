#!/usr/bin/env bash
# Generates an index webpage for each release tag.

for tagpath in apis/*; do
    tag=$(basename $tagpath)
    ./generate-tag-index.py "$tag" > "tags/$tag.html"
done
