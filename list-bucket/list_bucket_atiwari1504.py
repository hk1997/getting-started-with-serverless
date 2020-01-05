import json
import boto3
s3 = boto3.resource('s3')
def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('firstatiwari1504')
    file_count=0
    for file in my_bucket.objects.all():
        print(file.key)
        file_count+=1
    print('Total Number of files = {}'.format(file_count))
