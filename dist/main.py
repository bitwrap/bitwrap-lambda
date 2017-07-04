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

OPTIONS = {
    'pg-host': os.environ.get('RDS_HOST', '127.0.0.1'),
    'pg-port': os.environ.get('RDS_PORT', 5432),
    'pg-username': os.environ.get('RDS_USER', 'postgres'),
    'pg-password': os.environ.get('RDS_PASS', 'bitwrap'),
    'pg-database': os.environ.get('RDS_DB', 'bitwrap')
}

def eventstore(schema):
    """ get eventstore handle """
    return psql.Storage(schema, **OPTIONS)

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

def dispatch_route(store, event, params):
    payload = event.get('body')

    if payload == '' or payload is None:
        payload = "{}"

    return store.commit({
        'oid': params['oid'],
        'action': params['action'],
        'payload': payload
    })

def event_route(store, event, params):
    return store.db.events.fetch(params['eventid'])

def stream_route(store, event, params):
    return store.db.events.fetchall(params['streamid'])

def machine_route(store, event, params):
    machine = pnml.Machine(params['schema'])
    return {'machine':{
               'name': params['schema'],
               'places': machine.net.places,
               'transitions': machine.net.transitions}}

def schemata_route(store, event, params):
    return {'schemata': ptnet.schema_list()}

def state_route(store, event, params):
    return store.db.states.fetch(params['oid'])

def handler(event, context):
    """ handle events routed from gateway api """
    func = event['resource'].split('/')[1] + '_route'
    epp = event.get('pathParameters')

    if epp is None:
        epp = {}

    schema = epp.get('schema')

    if schema:
        store = eventstore(schema)
    else:
        store = None

    return success(globals()[func](store, event, epp))
