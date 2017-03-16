import os
import requests

WRITE_KEY =  os.environ.get('KEEN_API_KEY', None)
PROJECT =  os.environ.get('KEEN_PROJECT', None)

API_URL = 'http://api.keen.io/3.0/projects/%s/events/%s'

def post(body, schema='bitwrap'):

    if PROJECT:

        uri = (API_URL % ( PROJECT, schema )).encode('latin-1')

        return requests.post(
            uri,
            headers={
                'Authorization': [WRITE_KEY],
                'Content-Type': ['application/json']
            },
            data=body
        )
