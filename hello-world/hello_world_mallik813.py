import json

def first_pr(event, context):
    print("Hello World! from team UNCERTAINERS")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }