"""
Lambda handler for bitwrap gateway api.

https://github.com/bitwrap/bitwrap-io/blob/master/bitwrap_io/_lambda.py
"""

from bitwrap_io import _lambda
import keen

def handler(event, context):

    res = _lambda.handler(event, context)

    if event['path'] == '/api' and 'body' in res:
        keen.post(res['body'], schema=event['pathParameters']['schema'])

    return res
