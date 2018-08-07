#!/usr/bin/env bash
# Dumps list of API calls in each bitcoin release to a file named with release tag.

function dump {
    git clean -fdx
    git checkout "$1"
    git grep --files-with-matches "static const CRPCCommand .*\[\] =" *.cpp | xargs cat | ../dumpapi.py > "../apis/$1"

    mkdir -p "../docdata/$1/"
    cat "../apis/$1" | cut -f 1 | while read call; do
        git grep --files-with-matches "$call(" *.cpp >> targets
    done

    githash=$(git rev-parse HEAD)

    sort targets | uniq | while read filepath; do
        ../dumpdocs.py "../docdata" "$1" "$filepath" "$githash" < "$filepath"
    done
    rm targets
}

cd bitcoin
for release in `git tag | grep --extended-regexp "^v[0-9]+\.[0-9]+\.[0-9]+$"`; do
    dump "$release"
done

dump "master"