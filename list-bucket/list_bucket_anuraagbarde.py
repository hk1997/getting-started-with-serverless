import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('anuraagkibaalti1') 
    count=0
    k=[]
    for obj in bucket.objects.all():
        k.append(obj.key)
        count+=1
    print("Total No of objects =",count)
    print(k)
    
    return {
        'statusCode': 200,
        'data' : k,
    }
