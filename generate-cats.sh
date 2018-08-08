#!/usr/bin/env bash
# Generates an API doc chart for each category.

mkdir -p cats
for cat in $(cut -f 3 apis/* | sort | uniq); do
    ./generate-index.py "$cat" > "cats/$cat.html"
done
