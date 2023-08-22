#!/bin/bash

trap 'rm -f "$TMPFILE"' EXIT

set -e
set -x

TMPFILE=$(mktemp -t requirements-XXXXXX.txt)

poetry export --with dev --without-hashes -f requirements.txt -o $TMPFILE
# Somehow poetry exports zope.interface as zope-interface and liccheck does not
# like it.
sed -i -e "s/zope-interface/zope.interface/g" $TMPFILE
poetry run liccheck -r $TMPFILE
