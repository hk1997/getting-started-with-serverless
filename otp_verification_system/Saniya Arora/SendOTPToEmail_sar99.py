import json
import boto3
import random
import decimal
import time
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    email = event['queryStringParameters']['email']
    otp = random.randrange(10000, 99999)
    expiry = time.time() + 300
    flag = 0
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OTP_verification')
    response = table.query(
        KeyConditionExpression=Key('ContactDetails').eq(email)
    )   
    if len(response['Items'])==1:
        if response['Items'][0]['IsVerified'] == True:
            Response = {}
            Response['Message'] = "Hooray! You are already verified!"
        elif int(response['Items'][0]['NoOfTries']) >= 3:
            Response = {}
            Response['Message'] = "Sorry! You have reached the maximum number of allowed tries"
        else: 
            flag=1
            Response = {}
            Response['Message'] = "Your OTP has been sent to your email"
            response = table.update_item(
                Key={
                    'ContactDetails': email,
                },
                UpdateExpression="set OTP = :o, NoOfTries=:n, Expiry=:e",
                ExpressionAttributeValues={
                    ':o': str(otp),
                    ':e': str(expiry),
                    ':n': str(int(response['Items'][0]['NoOfTries']) + 1)
                },
                ReturnValues="UPDATED_NEW"
            )
        
        
    elif len(response['Items'])==0:
        item = table.put_item(
            Item={
                'ContactDetails': email,
                'Expiry': str(expiry),
                'IsVerified': False,
                'OTP': str(otp),
                'NoOfTries': str(1)
            }
        )
        flag=1
        Response = {}
        Response['Message'] = "Your OTP has been sent to your email"
        
    if flag==1:
        SENDER = "saniya.rishi@gmail.com"
        RECIPIENT = email
        AWS_REGION = "us-west-2"
        SUBJECT = "Your One Time Password (OTP)"
    
        body = "Your One Time Password(OTP) is " + str(otp) + ". This password expires within 5 minutes. You have at max three tries. "
        BODY_TEXT = body
    
        CHARSET = "utf-8"
    
        client = boto3.client('ses',region_name=AWS_REGION)
    
    
        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
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
        'body': json.dumps(Response)
    }
       
        
