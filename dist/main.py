"""
Lambda handler for bitwrap gateway api
Forwards transform events to keen.io

Configure by setting env vars:

export KEEN_PROJECT='aaaaaaaaaaaaaaaaaaaaaaaa'
export KEEN_API_KEY='xxxxxxxx...xxxxxxxxxxxxxxx'

"""

import requests
import os
import json
#from bitwrap_io.rpc import eventstore, call
import bitwrap_machine as pnml
from bitwrap_machine import ptnet

WRITE_KEY =  os.environ.get('KEEN_API_KEY', None)
PROJECT =  os.environ.get('KEEN_PROJECT', None)
API_URL = 'http://api.keen.io/3.0/projects/%s/events/%s'

options = {
    'pg-host': '127.0.0.1',
    'pg-port': 5432,
    'pg-username': 'postgres',
    'pg-password': 'bitwrap',
    'pg-database': 'bitwrap'
}


def post(body, schema='bitwrap'):
    """ forward event to keen.io """

    if PROJECT:
        pass

    uri = (API_URL % ( PROJECT, schema )).encode('latin-1')

    return requests.post(
        uri,
        headers={
            'Authorization': WRITE_KEY,
            'Content-Type': 'application/json'
        },
        data=body
    )

# TODO: convert this to a handler in the same style as bitwrap-io.api.rpc
def handler(event, context):
    """ handle events routed from gateway api """

    res = _lambda.handler(event, context)

    if event['path'] == '/api' and 'body' in res:
        # XXX: deserializing jason again
        # ? instead should add & tap into a header? x-bitwrap-schema: 'counter' ?
        _schema = json.loads(event['body'])['params'][0]['schema']
        post(res['body'], schema=_schema)


    return res
