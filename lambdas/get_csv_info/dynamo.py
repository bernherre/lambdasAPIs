#import awswrangler as wr
import os
import boto3
import pandas as pd
from boto3.dynamodb.conditions import Key, Attr

s3 = boto3.client('s3')
session_prod = boto3.Session()
s3_resource = boto3.resource('s3')
dynamodb_prod = session_prod.resource('dynamodb')
s3 = session_prod.client('s3')
def read_dynamo(dynamodb_prod, tablename,ticker,datestart,dateend):
    table = dynamodb_prod.Table(tablename)
    response = table.scan(FilterExpression = Attr("ticker").is_in(ticker) & Attr("date").between(datestart,dateend))
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    df = pd.DataFrame(data)
    return df
def createUrl(s3_resource,bucket, key, timeInSeconds):
        #### previous variables including aws sessions###
    urle = s3.generate_presigned_url('get_object',Params={'Bucket': bucket, 'Key': key}, ExpiresIn = timeInSeconds)
    print('urle: '+urle)
    return urle