#!/usr/bin/env bash
# Dumps list of API calls in each bitcoin release to a file named with release tag.

function dump {
    git checkout "$1"
    git grep --files-with-matches "static const CRPCCommand .*\[\] =" *.cpp | xargs cat | ../dumpapi.py > "../apis/$1"

    mkdir -p "../docs/$1/"
    git grep --files-with-matches "static const CRPCCommand .*\[\] =" *.cpp | xargs cat | ../dumpdocs.py "../docs" "$1"
}

cd bitcoin
for release in `git tag | grep --extended-regexp "^v[0-9]+\.[0-9]+\.[0-9]+$"`; do
    dump "$release"
done

dump "master"