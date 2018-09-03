import json
import datetime
from boto3 import dynamodb 

def handler(event, context):
    client = boto3.client('dynamodb')
    response = client.get_item(TableName='Sketches', Key={'topic':{'S':"bernardPenisSuckByManyMen"}})

    data = {
        'response': str(response),
        'context': context,
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}