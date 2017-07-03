""" bitwrap.test.test_machine """
import os
import sys
import json
import unittest

sys.path.append(os.path.abspath(__file__ + '/../'))
import mocks
sys.path.append(os.path.abspath(__file__ + '/../../dist'))
import main as Api

class LamdaTest(unittest.TestCase):
    """ test api methods not dealing with events"""

    def test_lambda_handler(self):
        """ test a sequence of tic-tac-toe transformations """

        res = Api.handler(mocks.API_POST, {})
        print json.loads(res)['event']

        # KLUDGE: do an actual test
        #self.assertTrue(data['error'] is None)
        #print json.dumps(data, indent=4)

if __name__ == '__main__':
    unittest.main()
