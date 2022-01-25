import os
import boto3
import traceback
import json
from boto3.dynamodb.conditions import Key

def query_SpeedTestResults(dydbClient, dbTable):
    table = dydbClient.Table(dbTable)
    response = table.scan()
    return response['Items']

def handler(event, context):
    
    try:
        TABLE_NAME = os.getenv('TABLE_NAME')
        dynamo = boto3.resource('dynamodb')
        res = query_SpeedTestResults(dynamo, TABLE_NAME)
        body_str = '{'
        for i in res[-24:]:
            body_str += '{"t":' +str(i['TimeStamp'])+ ', "dw": ' + str(i['DownloadSpeed']) + ', "up": ' + str(i['UploadSpeed']) + '},'
        body_str = body_str[:-1] + '}'
    except Exception as e:
        return {'statusCode': 502,
                'body': 'Exception: ' + str(e) + '\nTraceback: ' + traceback.format_exc(),
                'headers': {'Content-Type': 'application/json'}
        }

    return {'statusCode': 200,
            'body': body_str,
            'headers': {'Content-Type': 'application/json'}
    }