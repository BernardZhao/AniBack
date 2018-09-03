import json
import datetime
import boto3

def handler(event, context):
  try:
    requestType = event["httpMethod"]
    path = event["path"]
    client = boto3.client('dynamodb')

    response = {}

    if path == "/":
      response = {
        "validEndpoints":["/sketches"]
      }
  
    elif path == "/sketches":
        if requestType == "GET":

          if event["queryStringParameters"]:
            record = client.get_item(TableName='Sketches', Key={'sketchId':{'S':event["queryStringParameters"]["sketchId"]}})
            response = {
              'description': record['Item']['description']['S'],
              'sketchId': record['Item']['sketchId']['S'],
              'title': record['Item']['title']['S'],
            }

          else:
            paginator = client.get_paginator('scan')
            response["items"] = []
            for page in paginator.paginate(TableName='Sketches'):
              for record in page["Items"]:
                response["items"].append(record)


  
  except:
    pass
  
  return {'statusCode': 200,
          'body': json.dumps(response),
          'headers': {'Content-Type': 'application/json'}}

