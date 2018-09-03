import json
import datetime
import boto3

client = boto3.client('dynamodb')

def root(action, params):
  return {
    "validEndpoints": routes.keys()
  }

def sketches(action, params):
  if action == "GET":
    if params:
      record = client.get_item(
        TableName='Sketches',
        Key={'sketchId':{'S':params["sketchId"]}}
      )
      return {
        'description': record['Item']['description']['S'],
        'sketchId': record['Item']['sketchId']['S'],
        'title': record['Item']['title']['S'],
      }
    else:
      paginator = client.get_paginator('scan')
      response = {
        "items": []
      }
      for page in paginator.paginate(TableName='Sketches'):
        for record in page["Items"]:
          response["items"].append(record)
      return response

def handler(event, context):
  try:
    response = routes[event["path"]](event["httpMethod"], event["queryStringParameters"])
  except Exception as e:
    return {'statusCode': 500,
            'body': str(e),
            'headers': {'Content-Type': 'application/json'}}
  return {'statusCode': 200,
          'body': json.dumps(response),
          'headers': {'Content-Type': 'application/json'}}

routes = {
  "/": root,
  "/sketches": sketches
}