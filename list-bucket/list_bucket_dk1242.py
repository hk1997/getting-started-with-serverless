import json
import boto3
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    bucket = s3.Bucket('issue2s3')
    for obj in bucket.objects.all():
        print(obj.key)
     
    return {
        'statusCode': 200,
        'body': json.dumps('See logs for the content of bucket')
    }