import json
import datetime
import boto3

client = boto3.client('dynamodb')
s3 = boto3.resource('s3')

def root(action, params):
  return {
    "validEndpoints": list(routes.keys())
  }

def sketches(action, params):
  if action == "GET":
    if params:
      record = client.get_item(
        TableName='Sketches',
        Key={'sketchId':{'S':params["sketchId"]}}
      )
      response = {
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

def frames(action, params):
  if action == "GET":
    if params:
      record = client.get_item(
        TableName='Frames',
        Key={
              'sketchId':{
                'S':params["sketchId"]
                },
              'frameId':{
                'S':params["frameId"]
              }
            }
      )

      response = {
        'sketchId': record['Item']['sketchId']['S'],
        'frameId': record['Item']['frameId']['S'],
        'author': record['Item']['author']['S'],
        'imagePath': record['Item']['imagePath']['S']
      }
      
    else:
      paginator = client.get_paginator('scan')
      response = {
        "items": []
      }
      for page in paginator.paginate(TableName='Frames'):
        response["items"] += page["Items"]

  else:
    response = {
      "items": []
    }
  
  return response

def imagesPaths(action, params):
  if action == "GET":
    if params:
      record = client.get_item(
        TableName='Frames',
        Key = {
              'sketchId':{
                'S':params["sketchId"]
                },
              'frameId':{
                'S':params["frameId"]
              }
            }
      )

      response = {
        'imagePath': record['Item']['imagePath']['S']
      }
      
    else:
      response = {
        "items":[]
      }

      page = client.query(
          TableName="Frames",
          Select="SPECIFIC_ATTRIBUTES",
          AttributesToGet=['imagePath'],
          KeyConditionExpression="sketchId = :"+record['Item']['sketchId']['S']
      )
      
      while page.get('LastEvaluatedKey'):
        response["items"] += page["Items"]
        page = client.query(
          TableName="Frames",
          Select="SPECIFIC_ATTRIBUTES",
          AttributesToGet=['imagePath'],
          ExclusiveStartKey=page['LastEvaluatedKey'],
          KeyConditionExpression="sketchId = :"+record['Item']['sketchId']['S']
        )

  else:
    response = {
      "items": []
    }
  
  return response

def image(action, params):
  if action == "GET":
    if params:
      imagePath = params["imagePath"]
      #Get base 64 string given path from s3 bucket and store in string
      s3.Bucket('mybucket').download_file(imagePath, '/tmp/img.tmp')

      base64 = ""

      with open("/tmp/img.tmp", "rb") as image_file:
        base64 = base64.b64encode(image_file.read())
      
      response = {
        'imageSource': base64
      }
      
    else:
      response = {
        "items":[]
      }

  else:
    response = {
      "items": []
    }
  
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
  "/sketches": sketches,
  "/frames": frames,
  "/imagePaths": imagePaths,
  "/image": image
}