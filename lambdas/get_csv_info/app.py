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
        print(event)
        parameter= main_functions.get_param(event, event_type='pathParameters', param_name='fechast')
        print(parameter)
        lista=parameter.split(';')
        print(lista)
        main_functions.set_ticker(ticker=lista[0])
        main_functions.set_startdate(startdate=lista[1])
        main_functions.set_enddate(enddate=lista[2])
        print(os.environ['dynamodb_table'],os.environ['s3_bucket'])
        response_body = main_functions.info_tickers(dynamodb_prod=dynamodb_prod,tablename=os.environ['dynamodb_table'],ticker='['+str(lista[0])+']',startdate=str(lista[1]),enddate=str(lista[2]),bucket=os.environ['s3_bucket'])
        return response_body
        
    except Exception as e:
        return json.dumps([{"error":e}], default=str)
