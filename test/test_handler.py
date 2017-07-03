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

class LamdaTest(unittest.TestCase):
    """ test api methods not dealing with events"""

    def setUp(self):
        pg.create_db(pnml.Machine('counter'), drop=True, **Api.options)
        self.store = Api.eventstore('counter')
        self.store.db.create_stream('foo')


    def test_lambda_handler(self):
        """ test a sequence of tic-tac-toe transformations """

        res = Api.handler(mocks.API_POST, {})
        data = json.loads(res['body'])
        print json.dumps(data, indent=4)
        self.assertTrue(data.get('__err__', None) is None)

if __name__ == '__main__':
    unittest.main()
