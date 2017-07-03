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
import bitwrap_machine as pnml
from bitwrap_machine import ptnet
import bitwrap_psql as psql

WRITE_KEY =  os.environ.get('KEEN_API_KEY', None)
PROJECT =  os.environ.get('KEEN_PROJECT', None)
API_URL = 'http://api.keen.io/3.0/projects/%s/events/%s'

options = {
    'pg-host': os.environ.get('RDS_HOST', '127.0.0.1'),
    'pg-port': os.environ.get('RDS_PORT', 5432),
    'pg-username': os.environ.get('RDS_USER', 'postgres'),
    'pg-password': os.environ.get('RDS_PASS', 'bitwrap'),
    'pg-database': os.environ.get('RDS_DB', 'bitwrap')
}

def eventstore(schema):
    """ get eventstore handle """
    return psql.Storage(schema, **options)

def post(body, schema):
    """ forward event to keen.io """

    if PROJECT is not None:
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


def success(body):
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(body)
    } 


# TODO: convert to hacked up dispatch similar to bitwrap_io.api.rpc
def handler(event, context):
    """ handle events routed from gateway api """
    
    if 'body' in event and event['body'] is not None:
        data = event['body']
    else:
        data = '{}'
        
    epp = event['pathParameters']
    res = eventstore(epp['schema']).commit({
        'oid': epp['oid'],
        'action': epp['action'],
        'payload': data
    })

    return success(res)
