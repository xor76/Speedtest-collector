import json
import os
import boto3
import dateutil.parser as dp

TABLE_NAME = os.getenv('TABLE_NAME')
dynamo = boto3.client('dynamodb')

def storeSpeedTestResultDB(speedTestResultJson, dbTable):
        timestamp_p = dp.parse(speedTestResultJson['timestamp'])
        response = dynamo.put_item(TableName=dbTable,
                               Item={
                                   'ResultID': {"S": str(speedTestResultJson['result']['id'])},
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

def handler(event, context):
    
    storeSpeedTestResultDB(event, TABLE_NAME)
    
    return {'statusCode': 200,
            'body': json.dumps(event),
            'headers': {'Content-Type': 'application/json'}
            }
