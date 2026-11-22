#!/bin/bash
cd "$(dirname "$0")/.."
for name in server game home; do
    echo "$name"
    bash run.sh -o "out/$name.xml" < "tests/examples/$name.conf"
    cat "out/$name.xml"
    echo
done