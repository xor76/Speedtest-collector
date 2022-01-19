import os
import boto3
import traceback

def storeSpeedTestResultDB(speedTestResultJson, dydbClient, dbTable):
    print("1nside store func"+'-'*20)
    print(speedTestResultJson)
    response = dydbClient.put_item(TableName=dbTable,
                               Item=speedTestResultJson
                            )
    return response

def handler(event, context):
    
    try:
        TABLE_NAME = os.getenv('TABLE_NAME')
        dynamo = boto3.client('dynamodb')
        res = storeSpeedTestResultDB(event['body'], dynamo, TABLE_NAME)

    except Exception as e:
        return {'statusCode': 502,
                'exception': str(e),
                'traceback': traceback.format_exc()
        }

    return {'statusCode': 200,
            'body': { "message": "Result inserted correctly in db table" },
            'headers': {'Content-Type': 'application/json'}
    }
