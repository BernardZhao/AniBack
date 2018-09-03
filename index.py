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
          record = client.get_item(TableName='Sketches', Key={'sketchId':{'S':event["queryStringParameters"]["sketchId"]}})

          response = {
            'description': record['Item']['description']['S'],
            'sketchId': record['Item']['sketchId']['S'],
            'title': record['Item']['title']['S'],
          }
  
  except:
    pass
  
  return {'statusCode': 200,
          'body': json.dumps(response),
          'headers': {'Content-Type': 'application/json'}}

