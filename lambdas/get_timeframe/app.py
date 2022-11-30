import boto3
import main
import json
import os

s3 = boto3.client('s3')
session_prod = boto3.Session()
s3_resource = boto3.resource('s3')
dynamodb_prod = session_prod.resource('dynamodb')
s3 = session_prod.client('s3')

main_functions = main.Main()


def handler(event, context):

    try:
        print(os.environ['dynamodb_table'])
        print(dynamodb_prod)
        ticker= main_functions.get_param(
            event, event_type='pathParameters', param_name='ticker')
        main_functions.set_ticker(ticker=ticker)
        response_body = main_functions.info_tickers(dynamodb_prod=dynamodb_prod,tablename=os.environ['dynamodb_table'],ticker=ticker)
        return response_body
        
    except Exception as e:
        return json.dumps([{"error":e}], default=str)
