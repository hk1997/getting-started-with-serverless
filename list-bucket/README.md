# Listing Bucket Contents
Write a lambda to list the contents of the bucket.
We will learn about IAM roles and policies and how to give lambda permission to use other aws services.

## Readings:

It is suggested to read of IAM roles and policies.
https://aws.amazon.com/iam/

## Guide:
You need to do the following:
- Go to S3 and create a bucket.
- Push some files to your S3 bucket.
- Go to IAM and create a role and attach S3 read access policy to that role.
- Go to lambda console and create a lambda function with the language of your choice.
- Provide your role to the lambda function.
- Use AWS API's  ( eg boto3 for python) to list the contents of your bucket through lambda.

## Contributions Guidelines
Please name your file as list_bukcet_(gthubhandle)

Eg. list_bucket_hk1997.py
