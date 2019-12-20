import boto3

s3 = boto3.resource('s3')
bucket = s3.Bucket('issue-2')

def lambda_handler(event, context):
    content = {}
    content['statusCode']=200
    i=0
    for object in bucket.objects.all():
        content[i]=object.key
        i=i+1
    return content
            
