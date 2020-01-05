import json
def lambda_handler(event, context):
    print('\n Hello World!')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello World!')
    }
