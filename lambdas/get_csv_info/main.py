#import awswrangler as wr
import os
import boto3
import pandas as pd
from dynamo import read_dynamo,createUrl
from boto3.dynamodb.conditions import Key, Attr
import time
import json 

s3 = boto3.client('s3')
session_prod = boto3.Session()
s3_resource = boto3.resource('s3')
dynamodb_prod = session_prod.resource('dynamodb')
s3 = session_prod.client('s3')

class Main:
    def __init__(self, ticker=None, startdate=None, enddate=None):
        self._ticker = ticker
        self._startdate=startdate
        self._enddate=enddate

    def set_ticker(self, ticker):
        print("El id a asignar es ", ticker)
        self._ticker = ticker

    def get_ticker(self):
        return self._ticker

    def set_startdate(self, startdate):
        print("La startdate ", startdate)
        self._startdate = startdate

    def get_startdate(self):
        return self._startdate

    def set_enddate(self, enddate):
        print("La enddate ", enddate)
        self._enddate = enddate

    def get_enddate(self):
        return self._enddate
        
    @staticmethod
    def get_param(event, event_type, param_name):
        return str(event[event_type][param_name])

    def info_tickers(self,dynamodb_prod, tablename,ticker,startdate,enddate,bucket):
        ticker=self.get_ticker()
        print(ticker)
        startdate=self.get_startdate()
        print(startdate)
        enddate=self.get_enddate()
        print(enddate)
        url=None
        tickers=ticker.split(',')
        print(tickers)
        df=read_dynamo(dynamodb_prod, tablename,tickers,startdate,enddate)
        from time import gmtime, strftime
        date=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        TEMP_FILENAME = '/tmp/export.csv'
        OUTPUT_KEY = 'export'+date+'.csv'
        df.to_csv(TEMP_FILENAME, index=False, header=True)
        s3_resource.Bucket(bucket).upload_file(TEMP_FILENAME, OUTPUT_KEY)
        url=createUrl(s3,bucket, OUTPUT_KEY, 360)
        request_response = {
            'statusCode': 200,
            'body': str(url)
                }
        return request_response