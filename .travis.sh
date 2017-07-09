#!/usr/bin/env bash

if [[ "${VIRTUAL_ENV}x" == "x" ]] ; then
  virtualenv .venv
  source .venv/bin/activate
fi

# build lambda package
pip install -e git+https://github.com/bitwrap/bitwrap-machine.git#egg=bitwrap-machine
pip install -e git+https://github.com/bitwrap/bitwrap-psql.git#egg=bitwrap-psql

cp -r $VIRTUAL_ENV/src/bitwrap-machine/bitwrap_machine  dist/
cp -r $VIRTUAL_ENV/src/bitwrap-psql/bitwrap_psql  dist/

pip install -t $PWD/dist pg8000==1.10.6
