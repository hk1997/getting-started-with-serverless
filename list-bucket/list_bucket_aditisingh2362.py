import json
import boto3
from boto3 import client
from botocore.exceptions import ClientError
import logging


s3 = boto3.resource('s3')
conn = client('s3')


def lambda_handler(event, context):
    SENDER = "aditisingh2362@gmail.com"
    RECIPIENT = "aditisingh2362@gmail.com"
    AWS_REGION = "us-west-2"
    SUBJECT = "Sending the bucket's content."
    record=event['Records'][0]
    bucket=record['s3']['bucket']['name']
    objects = [key['Key'] for key in conn.list_objects(Bucket=bucket)['Contents']]
    BODY_TEXT = "Contents:\n"
    index=0
    for obj in objects:
        index+=1
        BODY_TEXT=BODY_TEXT+str(index)+". "+str(obj)+"\n"
            
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        #Provide the contents of the email.
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
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
