import json
import boto3
import os


def lambda_handler(event, context):
    # TODO implement
    print(event)
    parameter=event['pathParameters']['token']
    print(parameter)
    lista=parameter.split('-')
    print(lista)
    print(os.environ['cognito_pool_id'])
    print(os.environ['cognito_pool_id'])
    responce=authenticate_and_get_token(username= str(lista[0]), password= str(lista[1]), user_pool_id= os.environ['cognito_pool_id'], app_client_id= os.environ['cognito_client_id'])
    return {
        'statusCode': 200,
        'body': json.dumps(responce)
    }



def authenticate_and_get_token(username: str, password: str, 
                               user_pool_id: str, app_client_id: str) :
    client = boto3.client('cognito-idp')

    resp = client.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=app_client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password
        }
    )

    print("Log in success")
    print("Access token:", resp['AuthenticationResult']['AccessToken'])
    print("ID token:", resp['AuthenticationResult']['IdToken'])
    return resp['AuthenticationResult']['IdToken']