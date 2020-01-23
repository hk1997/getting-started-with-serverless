import json
import boto3
import random 
from boto3 import client
from botocore.exceptions import ClientError
import logging
from boto3.dynamodb.conditions import Key, Attr
from time import time
AWS_REGION="us-east-1"
sns = boto3.client('sns',region_name=AWS_REGION)
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table('MobileOTP01')
ToSend=0

def lambda_handler(event, context):
    otp=random.randrange(100000, 999999)
    number=event["multiValueQueryStringParameters"]["number"][0]
    
    sns.set_sms_attributes(
           attributes={"DefaultSMSType": "Transactional"}
    )
    try:
        r1 = table.query(
            KeyConditionExpression=Key('number').eq(number) ,
        )
    except ClientError as e1:
        print(e1.response['Error']['Message'])
    else :
        print(r1)
    
    expiry = time() + 300
    if len(r1['Items']) == 0 :
        try:
            r2 = table.put_item(
                Item={
                    'number': number,
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
                        'number': number,
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
            response = sns.publish(
            PhoneNumber=number, 
            Message="The OTP is "+str(otp) + " This message is sent by Anurag Tiwari",
            )
        except ClientError as e3:
            print(e3.response['Error']['Message'])
        else:
            print("Message sent! Message ID:"),
            print(response['MessageId'])
            return {
                'statusCode': 200,
                'body': json.dumps('SMS Sent to ' + number + ' successfully!')
            }
                
