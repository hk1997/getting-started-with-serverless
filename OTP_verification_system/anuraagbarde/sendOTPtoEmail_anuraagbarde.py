import boto3
import secrets
import string
import datetime
import time
import json

def generate_OTP():
    final_OTP = secrets.choice(range(10000, 99999))
    return final_OTP

def lambda_handler(event,  context):
    
    #get email from api
    API_email = event['queryStringParameters']['email']
    generated_OTP = generate_OTP()
    client_dynamodb = boto3.client('dynamodb')
    
    stored_response = client_dynamodb.get_item(
            TableName='OTP3_expiry_tries_01',
            Key={
                'email': {
                    'S': API_email
                }
            },
            ConsistentRead=True,
    )
    
    if 'Item' in stored_response:
        if stored_response["Item"]["verified_status"]["BOOL"] == True:
            return{
                'statusCode' : 200,
                'body' : json.dumps("Your email is already verified :)")
            }
    
        elif int(stored_response['Item']['tries']['N']) > 10:
            return{
                'statusCode' : 403,
                'body' : json.dumps("You have exceeded the number of tries, use a different email ID"),
            }
        elif int(stored_response['Item']['tries']['N']) > 0:
            current_tries = int(stored_response['Item']['tries']['N']) + 1
            current_epochtime = time.time()
            
            response_put_item = client_dynamodb.put_item(
                TableName='OTP3_expiry_tries_01',
                Item={
                    'email': {
                        'S': API_email,
                    },
                    'tries': {
                        'N': str(current_tries),
                    },
                    'epoch_time': {
                        'N': str(current_epochtime),
                    },
                    'OTP': {
                        'N': str(generated_OTP), 
                    },
                    'verified_status':{
                        'BOOL': False,
                    },
                },
            )
            
            #email body = OTP
            nowstime = datetime.datetime.now()
            EMAIL_BODY = str(" Your OTP is " + str(generated_OTP) + " generated at the time = " + str(nowstime + datetime.timedelta(seconds=19800))+ ". You have tried for " + str(current_tries) + " times. Max allowed is 10")
            
            #send email with email body
            client_ses = boto3.client('ses')
            
            response = client_ses.send_email(
                Destination={
                    'ToAddresses': [
                        API_email,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': EMAIL_BODY,
                        },
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': 'Your OTP :)',
                    },
                },
                Source='bcs_201810@iiitm.ac.in',
            )
    
    
    else:
        #insert generated/updated values into DynamoDB
        current_epochtime = time.time()
        current_tries = 1
    
        response_put_item = client_dynamodb.put_item(
        TableName='OTP3_expiry_tries_01',
        Item={
                'email': {
                    'S': API_email,
                },
                'tries': {
                    'N': str(current_tries),
                },
                'epoch_time': {
                    'N': str(current_epochtime),
                },
                'OTP': {
                    'N': str(generated_OTP), 
                },
                'verified_status':{
                    'BOOL': False,
                },
            },
        )
        
        #email body = OTP
        nowstime = datetime.datetime.now()
        EMAIL_BODY = str(" Your OTP is " + str(generated_OTP) + " generated at the time = " + str(nowstime + datetime.timedelta(seconds=19800)) + ". You have tried for " + str(current_tries) + " times. Max allowed is 10")
        
        #send email with email body
        client_ses = boto3.client('ses')
        
        response = client_ses.send_email(
            Destination={
                'ToAddresses': [
                    API_email,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': EMAIL_BODY,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': 'Your OTP :)',
                },
            },
            Source='bcs_201810@iiitm.ac.in',
        )
    
    
    return {
        'statusCode': 200,
        'body' : json.dumps("Your OTP has been sent! God I am so fucking happy this stupid function is working, I think i am Gonaa cry, lol XDXDXD"), 
    }
