""" bitwrap.test.test_machine """
import os
import sys
import json
from twisted.internet import defer
from twisted.trial.unittest import TestCase

sys.path.append(os.path.abspath(__file__ + '/../'))
import mocks
sys.path.append(os.path.abspath(__file__ + '/../../dist'))
import main as Api

class LamdaTest(TestCase):
    """ test api methods not dealing with events"""

    def test_lambda_handler(self):
        """ test a sequence of tic-tac-toe transformations """

        res = Api.handler(mocks.API_POST, {})
        data = json.loads(res['body'])

        self.assertTrue(data['error'] is None)
        print json.dumps(data, indent=4)
