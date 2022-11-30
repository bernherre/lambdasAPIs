#import awswrangler as wr
import os
import boto3
import pandas as pd
from dynamo import read_dynamo_tickers
import json

s3 = boto3.client('s3')
session_prod = boto3.Session()
s3_resource = boto3.resource('s3')
dynamodb_prod = session_prod.resource('dynamodb')
s3 = session_prod.client('s3')

class Main:


    def info_tickers(self,dynamodb_prod, tablename):
        data_tickers=None
        tickers=read_dynamo_tickers(dynamodb_prod,tablename)
        data_tickers=[str(element) for element in tickers]
        data_tickers=','.join(data_tickers)
        request_response = {
            'statusCode': 200,
            'body': json.dumps(data_tickers)
        }
        return request_response
