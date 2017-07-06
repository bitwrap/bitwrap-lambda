"""
Lambda handler for bitwrap gateway api
Configure by setting the RDS_* env vars in the OPTIONS below
"""

import os
import json
import bitwrap_machine as pnml
from bitwrap_machine import ptnet
import bitwrap_psql as psql

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

def success(body):
    return {
        "statusCode": 200,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": json.dumps(body)
    } 

def rpc_schema_exists(schema):
    """ test that an event-machine schema exists """
    return eventstore(schema).db.schema_exists()

def rpc_schema_create(schema):
    """ test that an event-machine schema exists """
    machine = pnml.Machine(schema)
    psql.db.create_schema(machine, **OPTIONS)
    return rpc_schema_exists(schema)

def rpc_schema_destroy(schema):
    """ test that an event-machine schema exists """
    psql.db.drop_schema(schema, **OPTIONS)
    return not rpc_schema_exists(schema)

def rpc_stream_exists(schema, oid):
    """ test that a stream exists """
    return eventstore(schema).db.stream_exists(oid)


def rpc_stream_create(schema, oid):
    """ create a new stream if it doesn't exist """
    return eventstore(schema).db.create_stream(oid)

def dispatch_route(store, event, params):
    payload = str(event.get('body'))

    if payload.startswith('json='):
        data = payload[5:]
    elif payload == '':
        data = "{}"
    else:
        data = payload

    return store.commit({
        'oid': params['oid'],
        'action': params['action'],
        'payload': data
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

    if event['resource'] == '/api':
        res = {}
        payload = str(event.get('body'))

        try:
            if payload.startswith('json='):
                rpc = json.loads(payload[5:])
            else:
                rpc = json.loads(payload)

            res['id'] = rpc.get('id')
            func = 'rpc_' + rpc['method']
            res['result'] = globals()[func](*rpc['params'])
            res['error'] = None
        except Exception as (ex):
            res['error'] = ex.message

        return success(res)

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
