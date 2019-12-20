import boto3
from botocore.exceptions import ClientError
import logging


s3 = boto3.resource('s3')


def lambda_handler(event, context):
    bucket = s3.Bucket(event['bucketname'])
    SENDER = "saniya.rishi@gmail.com"
    RECIPIENT = event['receiver']
    AWS_REGION = "us-west-2"
    SUBJECT = "Conetnts of the 'issue-2' bucket"

    i=1
    body = "Conetents of the 'issue-2 bucket are as follows: \n"
    for object in bucket.objects.all():
        body = body + str(i) + ". " + object.key + "\n"
        i += 1
    logging.debug('This is a debug message')   
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
