# bitwrap-lambda

[![Build Status](https://travis-ci.org/bitwrap/bitwrap-lambda.svg?branch=master)](https://travis-ci.org/bitwrap/bitwrap-lambda)

Bitwrap eventstore deployed to AWS using lambda, RDS (and eventually S3/Athena)

Learn more: http://bitwrap.io

#### install

Travis.ci job creates a lambda function that is then (manually)
configured as a target from Amazon API Gateway using the included swagger.yaml'

#### run locally

Set env vars:

    export RDS_HOST=bitwrap-io-qa.deadbeef.us-east-1.rds.amazonaws.com
    export RDS_DB=bitwrap
    export RDS_USER=postgres
    export RDS_PASS=bitwrap

Run test

   PYTHONPATH=./ python test/test_handler.py
