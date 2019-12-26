import json
import boto3
import random
import decimal
import time
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

session = boto3.Session(
    region_name="us-west-2"
)
sns_client = session.client('sns')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    phone_number = event['queryStringParameters']['phone_number']
    otp = random.randrange(10000, 99999)
    expiry = time.time() + 300
    flag = 0
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OTP_verification')
    response = table.query(
        KeyConditionExpression=Key('ContactDetails').eq(phone_number)
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
            Response['Message'] = "Your OTP has been sent to your phone number"
            response = table.update_item(
                Key={
                    'ContactDetails': phone_number,
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
                'ContactDetails': phone_number,
                'Expiry': str(expiry),
                'IsVerified': False,
                'OTP': str(otp),
                'NoOfTries': str(1)
            }
        )
        flag=1
        Response = {}
        Response['Message'] = "Your OTP has been sent to your phone number"
        
    if flag==1:
        body = "Your One Time Password(OTP) is " + str(otp) + ". This password expires within 5 minutes. You have at max three tries. "
        response = sns_client.publish(
        PhoneNumber=phone_number,
        Message=body,
        MessageAttributes={
            'AWS.SNS.SMS.SenderID': {
                'DataType': 'String',
                'StringValue': 'SENDERID'
            },
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Transactional'
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps(Response)
    }
    
       
        
