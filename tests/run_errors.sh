#!/bin/bash
cd "$(dirname "$0")/.."
for file in tests/examples/broken.conf tests/errors/*.conf; do
    echo "$file"
    bash run.sh -o out/e.xml < "$file"
    echo
done