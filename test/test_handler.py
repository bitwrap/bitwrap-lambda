""" bitwrap.test.test_machine """
import os
import sys
import json
import unittest
import bitwrap_psql.db as pg
import bitwrap_machine as pnml

sys.path.append(os.path.abspath(__file__ + '/../'))
import mocks
sys.path.append(os.path.abspath(__file__ + '/../../dist'))
import main as Api

# empty context
ctx = {}

def execute(request):
    res = Api.handler(request, ctx)
    data = json.loads(res['body'])
    print json.dumps(data, indent=4)
    return data

class LamdaTest(unittest.TestCase):
    """ test api methods not dealing with events"""

    def setUp(self):
        pg.create_db(pnml.Machine('counter'), drop=True, **Api.OPTIONS)
        self.store = Api.eventstore('counter')
        self.store.db.create_stream('foo')


    def test_event_sequence(self):
        """ test a sequence of tic-tac-toe transformations """

        # read machine list
        execute(mocks.event(**{
            'resource': '/schemata',
            'method': 'GET',
            'path': '/schemata',
            'pathparams': None
        }))

        # read machines
        execute(mocks.event(**{
            'resource': '/machine/{schema}',
            'method': 'GET',
            'path': '/machine/counter',
            'pathparams': {
                'schema': 'counter'
            }
        }))

        # dispatch
        data = execute(mocks.event(**{
            'body': { "test": "payload" },
            'resource': '/dispatch/{schema}/{oid}/{action}',
            'method': 'POST',
            'path': '/dispatch/counter/foo/INC_1',
            'pathparams': {
                'schema': 'counter',
                'oid': 'foo',
                'action': 'INC_0'
            }
        }))

        self.assertTrue(data.get('__err__') is None)

        # read state
        execute(mocks.event(**{
            'resource': '/state/{schema}/{oid}',
            'method': 'GET',
            'path': '/state/counter/foo',
            'pathparams': {
                'schema': 'counter',
                'oid': 'foo'
            }
        }))

        # read event
        execute(mocks.event(**{
            'resource': '/event/{schema}/{eventid}',
            'method': 'GET',
            'path': '/dispatch/counter/' + data['id'],
            'pathparams': {
                'schema': 'counter',
                'eventid': data['id']
            }
        }))

        # read stream
        execute(mocks.event(**{
            'resource': '/stream/{schema}/{streamid}',
            'method': 'GET',
            'path': '/stream/counter/foo',
            'pathparams': {
                'schema': 'counter',
                'streamid': 'foo'
            }
        }))



if __name__ == '__main__':
    unittest.main()
