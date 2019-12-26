import json
import boto3
from boto3.dynamodb.conditions import Key
import time

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        x= dynamodb.get_item(TableName='OTP', Key={'Phone number':{'N':event['number']}})
        l=x['Item']
    except:
        return "Given Phone number doesn't exist."
    else:
        t=x["Item"]["Try"]['N']
        times=x['Item']['ttl']['N']
        print(time.time())
        table = boto3.resource('dynamodb').Table('OTP')
        pn=int(event['number'])
        print(t)
        if int(t)<3 and time.time()<float(times):
            t=int(t)+1
            pn=int(event['number'])
            response = table.update_item(
                     Key={
                            'Phone number': pn
                        },
                        UpdateExpression="set Try = :r",
                        ExpressionAttributeValues={
                            ':r': t,
                        },
                        ReturnValues="UPDATED_NEW"
                    )
            if event["otp"] == x['Item']['OTP']['N']:
                    response = table.delete_item(
                                        Key={
                                            'Phone number': pn 
                                        }
                                    ) 
                    return "OTP is successfully verified."
            
            else:
                return "Retry."
        elif time.time()>float(times):
                return "Time limit expired"
        else:
            response = table.delete_item(
                                        Key={
                                            'Phone number': pn 
                                        }
                                    ) 
            return "You have already reached the limit. Your OTP is now deactivated."
