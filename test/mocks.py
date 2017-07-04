import json
from string import Template

tpl = Template("""
{
    "resource": "$resource",
    "requestContext": {
      "resourceId": "123456",
      "apiId": "1234567890",
      "resourcePath": "$resource",
      "httpMethod": "$method",
      "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
      "accountId": "123456789012",
      "identity": {
      },
      "stage": "dev"
    },
    "queryStringParameters": {
    },
    "headers": {
    },
    "httpMethod": "$method",
    "stageVariables": {
    },
    "path": "$path"
}
""")

def event(**kwargs):
    raw = tpl.substitute(**kwargs)
    evt = json.loads(raw)

    if kwargs.get('body') is not None:
      evt['body'] = json.dumps(kwargs['body'])

    evt['pathParameters'] = kwargs['pathparams']

    return evt
