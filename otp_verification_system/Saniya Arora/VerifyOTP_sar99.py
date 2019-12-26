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
    print(time.time())
    contact = event['queryStringParameters']['contact']
    otp = event['queryStringParameters']['otp']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OTP_verification')
    response = table.query(
        KeyConditionExpression=Key('ContactDetails').eq(contact)
    )   
    if len(response['Items'])==1:
        if decimal.Decimal(response['Items'][0]['IsVerified']) == True:
            Response = {}
            Response['Message'] = "You have already got yourself verified. You need not enter any OTP again."
        elif decimal.Decimal(response['Items'][0]['Expiry']) < time.time():
            Response = {}
            Response['Message'] = "Sorry! You have exceeded the 5 min time limit of verifying your OTP. Please try again."
        elif decimal.Decimal(response['Items'][0]['OTP']) == decimal.Decimal(otp) :
            Response = {}
            Response['Message'] = "Hooray! You have been verified."
            response = table.update_item(
                Key={
                    'ContactDetails': contact,
                },
                UpdateExpression="set IsVerified=:v",
                ExpressionAttributeValues={
                    ':v': True
                    
                },
                ReturnValues="UPDATED_NEW"
            )
        else:
            Response = {}
            Response['Message'] = "Oops! That's not the correct OTP. Try asking for an OTP again. The ealier OTP won't work anymore."
            response = table.update_item(
                Key={
                    'ContactDetails': contact,
                },
                UpdateExpression="set OTP=:o",
                ExpressionAttributeValues={
                    ':o': str(random.randrange(10000, 99999))
                    
                },
                ReturnValues="UPDATED_NEW"
            )
    else:
        Response = {}
        Response['Message'] = "Oops! You have not asked for an OTP yet. Try asking for one before verifying."    
    return {
        'statusCode': 200,
        'body': json.dumps(Response)
    }
       
