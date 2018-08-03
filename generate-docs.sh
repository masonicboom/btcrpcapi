#!/usr/bin/env bash
# Generates a doc webpage for each doc data file in docdata/.

for datafile in docdata/*/*.json; do
    version=$(basename $(dirname $datafile))
    filename=$(basename $datafile)
    mkdir -p "docs/$version"
    base="${filename%.*}"
    ./generate-doc.py < "$datafile" > "docs/$version/$base.html" &
done

wait