"""
Lambda handler for bitwrap gateway api.

https://github.com/bitwrap/bitwrap-io/blob/master/bitwrap_io/_lambda.py
"""

from bitwrap_io import _lambda

def handler(event, context):

    res = _lambda.handler(event, context)

    if event['path'] == '/api' and 'body' in res:
        print res['body']

    return res
