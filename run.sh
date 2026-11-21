#!/bin/bash
if command -v py >/dev/null 2>&1; then
    py src/main.py "$@"
else
    python3 src/main.py "$@"
fi