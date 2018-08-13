#!/usr/bin/env bash
# Extracts docs from bitcoin source code and loads into DB.

DBFILENAME=bitdocs.db

function load {
    tag="$1"
    DBFILE="../$DBFILENAME"

    echo "Loading $tag..."

    git reset --hard HEAD 2> /dev/null > /dev/null
    git clean -fdx 2> /dev/null > /dev/null
    git checkout "$tag" 2> /dev/null > /dev/null

    githash=$(git rev-parse HEAD)

    # Load release metadata.
    ../load-release.py "$DBFILE" "$tag" "$githash"

    # Load API metadata.
    git grep --files-with-matches "static const CRPCCommand .*\[\] =" *.cpp | xargs cat | ../load-release-api.py "$DBFILE" "$tag"

    # Load docs from each file with RPC functions.
    funcregex=$(../generate-func-regex.py "$DBFILE" "$tag")
    git grep --extended-regexp --files-with-matches "$funcregex" *.cpp | while read filepath; do
        ../load-docs.py "$DBFILE" "$tag" "$filepath" < "$filepath"
    done
}

./init-db.py "$DBFILENAME"

cd bitcoin
for release in `git tag | grep --extended-regexp "^v[0-9]+\.[0-9]+\.[0-9]+$"`; do
    load "$release"
done

load "master"