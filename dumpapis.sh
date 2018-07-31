#!/usr/bin/env bash
# Dumps list of API calls in each bitcoin release to a file named with release tag.

function dump {
    git clean -fdx
    git checkout "$1"
    git grep --files-with-matches "static const CRPCCommand .*\[\] =" *.cpp | xargs cat | ../dumpapi.py > "../apis/$1"

    mkdir -p "../docs/$1/"
    while read call; do
        git grep --files-with-matches "$call(" *.cpp >> targets
    done <"../apis/$1"
    sort targets | uniq | xargs cat | ../dumpdocs.py "../docs" "$1"
    rm targets
}

cd bitcoin
for release in `git tag | grep --extended-regexp "^v[0-9]+\.[0-9]+\.[0-9]+$"`; do
    dump "$release"
done

dump "master"