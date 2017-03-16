"""
Lambda handler for bitwrap gateway api
Forwards all transform events to keen.io

Configure by setting env vars:

export KEEN_PROJECT='aaaaaaaaaaaaaaaaaaaaaaaa'
export KEEN_API_KEY='xxxxxxxx...xxxxxxxxxxxxxxx'


See handler source for more details:
https://github.com/bitwrap/bitwrap-io/blob/master/bitwrap_io/_lambda.py
"""

import requests
import os
import ujson as json
from bitwrap_io import _lambda

WRITE_KEY =  os.environ.get('KEEN_API_KEY', None)
PROJECT =  os.environ.get('KEEN_PROJECT', None)

API_URL = 'http://api.keen.io/3.0/projects/%s/events/%s'

def post(body, schema='bitwrap'):

    if PROJECT:

        uri = (API_URL % ( PROJECT, schema )).encode('latin-1')

        return requests.post(
            uri,
            headers={
                'Authorization': WRITE_KEY,
                'Content-Type': 'application/json'
            },
            data=body
        )

def handler(event, context):

    res = _lambda.handler(event, context)

    if event['path'] == '/api' and 'body' in res:
        # XXX: deserializing jason again
        # ? instead should add & tap into a header? x-bitwrap-schema: 'counter' ?
        _schema = json.loads(event['body'])['params'][0]['schema']
        post(res['body'], schema=_schema)


    return res
