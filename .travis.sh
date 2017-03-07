#!/usr/bin/env bash

if [[ "${VIRTUAL_ENV}x" == "x" ]] ; then
  virtualenv .venv
  source .venv/bin/activate
fi

# build lambda package
pip install -t $PWD/dist -r requirements.txt
pip install -e git+https://github.com/bitwrap/bitwrap-io.git#egg=bitwrap_io
cp -r $VIRTUAL_ENV/src/bitwrap-io/bitwrap_io  dist/

# re-init the test db #
python -m bitwrap_io.storage.sql
