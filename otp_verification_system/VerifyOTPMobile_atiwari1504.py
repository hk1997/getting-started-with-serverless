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

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('MobileOTP01')

def lambda_handler(event, context):
    number = event["multiValueQueryStringParameters"]["number"][0]
    otp = event["multiValueQueryStringParameters"]["otp"][0]
    try:
        r1 = table.query(
            KeyConditionExpression=Key('number').eq(number)
        ) 
    except ClientError as e1:
        print(e1.response['Error']['Message'])
    else :
        print(r1)
      
    if len(r1['Items'])==1:
        if decimal.Decimal(r1['Items'][0]['expiry']) < time.time():
            return {
                'statusCode': 200,
                'body': json.dumps('Time Limit Exceeds! Please try Again'),
            }
        elif decimal.Decimal(r1['Items'][0]['otp']) == decimal.Decimal(otp) :
            try:
                r2 = table.delete_item(
                    Key={
                        'number': number,
                    },
                )
            except ClientError as e2:
                print(e2.response['Error']['Message'])
            else :
                print(r2)
                return {
                    'statusCode': 200,
                    'body': json.dumps('OTP Verfied Successfully!'),
                }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps('Incorrect OTP! Try Again or Ask for another OTP'),
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Ask For OTP First then Verify it!'),
        }
    
