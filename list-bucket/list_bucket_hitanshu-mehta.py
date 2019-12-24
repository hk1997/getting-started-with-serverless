import json
import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')

SENDER = "hitanshu99amehta@gmail.com"

RECIPIENT = "hitanshu99amehta@gmail.com"

AWS_REGION = "us-east-1"

SUBJECT = "list of objects present in the s3 bucket"


def lambda_handler(event,context):
    list_objects = []
    print(str(event))
    bucket = event['Records'][0]['s3']['bucket']['name']
    # print(bucket.name)
    # for obj in bucket.objects.all():
    #     # print(obj.key)
    #     list_objects.append(obj.key)
    obj = event['Records'][0]['s3']['object']['key']
    list_objects.append(obj)
    index = 0
    BODY_TEXT = "New object added in bucket "+ bucket +" :\n"
    for obj in list_objects:
        index += 1
        BODY_TEXT = BODY_TEXT + str(index) + ". " + str(obj) + "\n" 
      
    BODY_HTML = "<html><head></head><body><h1>List of objects in bucket</h1><p>"+BODY_TEXT+"</p></body></html>"
    
    CHARSET = "UTF-8"
    
    client = boto3.client('ses',region_name = AWS_REGION)
    
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
                    'Html':
                        {
                            'Charset' : CHARSET,
                            'Data' : BODY_HTML,
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
