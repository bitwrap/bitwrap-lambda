# bitwrap-lambda

[![Build Status](https://travis-ci.org/bitwrap/bitwrap-lambda.svg?branch=master)](https://travis-ci.org/bitwrap/bitwrap-lambda)

Bitwrap eventstore ported to aws using lambda, RDS (and eventually S3/Athena)

See the demo app to learn more: http://bitwrap.io

#### install

On AWS this repo uploads a single lambda function that is then (manually)
configured as a target from Amazon API Gateway.

#### run locally

Set env vars:

    export RDS_HOST=bitwrap-io-qa.deadbeef.us-east-1.rds.amazonaws.com
    export RDS_DB=mysql
    export RDS_USER=root
    export RDS_PASS=deadbeefdeadbeef

Drop & Create db

    # XXX THIS WILL DROP THE EXISTING DB!! XXX
    python -m bitwrap_io.storage.sql


Run the app

    BITWRAP_DATASTORE=mysql twist bitwrap --listen-port=8080 --listen-address=127.0.0.1

Run test

   BITWRAP_DATASTORE=mysql trial test/test_handler.py
