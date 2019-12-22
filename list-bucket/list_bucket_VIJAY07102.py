import json


def object_lists(event, context):
    import boto3
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('listingobjects')              #'listingobjects' is the bucket name 
    count=0
    k=[]
    for obj in bucket.objects.all():
        k.append(obj.key)
        count+=1
    print("Total No of objects =",count)
    print(k)
     
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
