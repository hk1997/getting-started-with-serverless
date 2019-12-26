import boto3
from botocore.exceptions import ClientError



s3 = boto3.resource('s3')


def lambda_handler(event, context):
    print(event)
    bucket = s3.Bucket("issue3ses")
    SENDER = "dhruval16kush@gmail.com"
    RECIPIENT = "dhruval16kush@gmail.com"
    AWS_REGION = "ap-south-1"
    SUBJECT = "Contents of s3 bucket"

    body = "Contents of s3 bucket are: \n"
    for object in bucket.objects.all():
        body = body + "#" + object.key + "\n"
  
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