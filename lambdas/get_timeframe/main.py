#import awswrangler as wr
import os
import boto3
import pandas as pd
from dynamo import read_dynamo_dates
from boto3.dynamodb.conditions import Key, Attr
import json 

s3 = boto3.client('s3')
session_prod = boto3.Session()
s3_resource = boto3.resource('s3')
dynamodb_prod = session_prod.resource('dynamodb')
s3 = session_prod.client('s3')

class Main:
    def __init__(self, ticker=None):
        self._ticker = ticker

    def set_ticker(self, ticker):
        print("El id a asignar es ", ticker)
        self._ticker = ticker

    def get_ticker(self):
        return self._ticker
        
    @staticmethod
    def get_param(event, event_type, param_name):
        return str(event[event_type][param_name])

    def info_tickers(self,dynamodb_prod, tablename,ticker):
        ticker=self.get_ticker()
        dates=None
        tickers=ticker.split(',')
        dates=read_dynamo_dates(dynamodb_prod, tablename,tickers)
        date=','.join(dates)
        date=date.strip('\"')
        request_response = {
            'statusCode': 200,
            'body': date
                }
        return request_response