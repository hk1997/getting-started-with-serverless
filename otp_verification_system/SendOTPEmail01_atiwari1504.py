import json
import boto3
import random 
from boto3 import client
from botocore.exceptions import ClientError
import logging
from boto3.dynamodb.conditions import Key, Attr
from time import time
AWS_REGION="ap-south-1"
SENDER = "atiwari1504@gmail.com"
# RECIPIENT = "anurag1504t@gmail.com"
SUBJECT = "OTP to Verify Email"
CHARSET = "UTF-8"
client = boto3.client('ses', region_name=AWS_REGION)

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('EmailOTP01')
ToSend=0

def lambda_handler(event, context):
    otp=random.randrange(100000, 999999)
    email=event["multiValueQueryStringParameters"]["email"][0]
    RECIPIENT=email
    BODY_TEXT="The OTP is "+str(otp) + " This message is sent by Anurag Tiwari"
    r1 = table.query(
        KeyConditionExpression=Key('email').eq(email) ,
    )
    
    
    expiry = time() + 300
    if len(r1['Items']) == 0 :
        try:
            r2 = table.put_item(
                Item={
                    'email': email,
                    'otp': str(otp),
                    'expiry': str(expiry),
                    'tries': 1,
                }
            )
        except ClientError as e2:
            print(e2.response['Error']['Message'])
        else :
            print(r2)
            ToSend=1
    else :      
        if r1['Items'][0]['tries'] > 3 :
            return {
                'statusCode': 200,
                'body': json.dumps('You have tried more than 3 Times!'),
            }
        else : 
            try:
                r3 = table.update_item(
                    Key={
                        'email': email,
                    },
                    UpdateExpression="set otp = :o, tries=:n, expiry=:e",
                    ExpressionAttributeValues={
                        ':o': otp,
                        ':e': str(expiry),
                        ':n': r1['Items'][0]['tries'] + 1
                    },
                    ReturnValues="UPDATED_NEW"
                )
            except ClientError as e4:
                print(e4.response['Error']['Message'])
            else :
                print(r3) 
                ToSend=1
    
    if ToSend == 1 : 
        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
            return {
                'statusCode': 200,
                'body': json.dumps('Email sent to '+ email +' successfully!'),
            } 
                
