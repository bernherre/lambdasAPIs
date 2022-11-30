from yahoo_fin.stock_info import *
import pandas as pd
from decimal import Decimal
from asyncore import write
import boto3
import pandas as pd
import datetime
from boto3.dynamodb.conditions import Key, Attr
session_prod = boto3.Session()#
s3_resource = boto3.resource('s3')
dynamodb_prod = session_prod.resource('dynamodb')
s3 = session_prod.client('s3')
##############################################################################
#                               2. Read data                                  #
###############################################################################
# Set label
stocks = ["AAPL"] # If you want to grab multiple stocks add more labels to this list
#AAPL---apple
#SEDG
#BABA
#DIS --walt disney
# Set start and end dates
df = get_data('AAPL', start_date='2022-11-14')
dfa['date']=dfa['date'].astype(str)
dfa['open']=dfa['open'].astype(str)
dfa['high']=dfa['high'].astype(str)
dfa['low']=dfa['low'].astype(str)
dfa['close']=dfa['close'].astype(str)
dfa['adjclose']=dfa['adjclose'].astype(str)
dfa['id']=(dfa['id']+12).astype(str)
dfa.dtypes

json_list = json.loads(json.dumps(list(dfa.T.to_dict().values())))
def write_dynamo(dynamodb_test, tablenameTarget, json_data):
    table = dynamodb_test.Table(tablenameTarget) 
    print(table)
    for item in json_data:
        print(item)
        response = table.put_item(Item=item)
        print(response)

write_dynamo(dynamodb_prod, 'data_inversion', json_list)