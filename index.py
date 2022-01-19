import os
import boto3
import dateutil.parser as dp
import traceback

def storeSpeedTestResultDB(speedTestResultJson, dydbClient, dbTable):
        timestamp_p = dp.parse(speedTestResultJson['timestamp'])
        response = dydbClient.put_item(TableName=dbTable,
                               Item={
                                   'ResultId': {"S": str(speedTestResultJson['result']['id'])},
                                   'DownloadSpeed': {"N": str(speedTestResultJson['download']['bytes'])},
                                   'TimeStamp': {"N": str(timestamp_p.timestamp())},
                                   'UploadSpeed': {"N": str(speedTestResultJson['upload']['bytes'])},
                                   'Latency': {"N": str(speedTestResultJson['ping']['latency'])},
                                   'Jitter': {"N": str(speedTestResultJson['ping']['jitter'])},
                                   'internalIp': {"S": str(speedTestResultJson['interface']['internalIp'])},
                                   'externalIp': {"S": str(speedTestResultJson['interface']['externalIp'])},
                                   'macAddr': {"S": str(speedTestResultJson['interface']['macAddr'])},
                                   'packetLoss': {"N": str(speedTestResultJson['packetLoss'])},
                                   'ServerName': {"S": str(speedTestResultJson['server']['name'])},
                                   'ServerHost': {"S": str(speedTestResultJson['server']['host'])},
                                   'ServerID': {"N": str(speedTestResultJson['server']['id'])},
                               }
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
