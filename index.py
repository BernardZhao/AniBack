import json
import datetime
import boto3

def handler(event, context):
    client = boto3.client('dynamodb')
    response = client.get_item(TableName='Sketches', Key={'sketchId':{'S':"bernardPenisSuckByManyMen"}})
    data = {
        'description': response['Item']['description']['S'],
        'sketchId': response['Item']['sketchId']['S'],
        'title': response['Item']['title']['S'],
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}

