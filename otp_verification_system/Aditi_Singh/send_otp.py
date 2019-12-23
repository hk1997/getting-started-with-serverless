import json
import boto3
import math, random 
from boto3 import client
from botocore.exceptions import ClientError
import logging
  
def generateOTP() : 
 
    digits = "0123456789"
    OTP = "" 
 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP 


dynamodb = boto3.client('dynamodb')
def lambda_handler(event, context):
   otp=generateOTP()
   SENDER = "aditisingh2362@gmail.com"
   RECIPIENT = event['email']
   AWS_REGION = "us-west-2"
   SUBJECT = "OTP Verification"
   BODY_TEXT="The OTP is "+str(otp)
   x= dynamodb.put_item(TableName='OTP', Item={'Phone number':{'N':event['number']},'Email':{'S':event['email']},'Try':{'N':'0'},'OTP':{'N':otp}})
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
   sns = boto3.client('sns',region_name=AWS_REGION)

   # Publish a simple message to the specified SNS topic
   try:
      response = sns.publish(
          PhoneNumber="+916388387503",
          Message="The OTP is "+str(otp),
      )
   except ClientError as e:
     print(e.response['Error']['Message'])
   else:
     print("Message sent! Message ID:"),
     print(response['MessageId'])
     return "Done!"
