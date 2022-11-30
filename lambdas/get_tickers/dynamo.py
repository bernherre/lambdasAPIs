#import awswrangler as wr
import os
import boto3
import pandas as pd

s3 = boto3.client('s3')
session_prod = boto3.Session()
s3_resource = boto3.resource('s3')
dynamodb_prod = session_prod.resource('dynamodb')
s3 = session_prod.client('s3')
def read_dynamo_tickers(dynamodb_prod, tablename):
        table = dynamodb_prod.Table(tablename)
        print(table)
        response = table.scan()
        print(response)
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        df = pd.DataFrame(data)
        df=df['ticker'].drop_duplicates()
        return df