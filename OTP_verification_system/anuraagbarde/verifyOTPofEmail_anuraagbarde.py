import json
import boto3
import string
import datetime
import time
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    
    hell = True
    
    #get email and OTP from api
    try:
        API_email = event['queryStringParameters']['email']
        unverifiedOTP = int(event['queryStringParameters']['OTP'])
    except Exception as e:
        return{ 
            'statusCode' : '403',
            'body' : json.dumps("There is a missing email or OTP in the POST request you have sent")
        }    
    
    current_epochtime = time.time()
    
    client_dynamodb = boto3.client('dynamodb')
    
    try:
        stored_response = client_dynamodb.get_item(
                TableName='OTP3_expiry_tries_01',
                Key={
                    'email': {
                        'S': API_email
                    }
                },
                ConsistentRead=True,
    )
    except Exception as e:
        return{
            'statusCode' : '500',
            'body' : "There is an error in contacting the database, Pls try again"
        }
    
    if 'Item' in stored_response:
        if stored_response["Item"]["verified_status"]["BOOL"] == True:
            return{
                'statusCode' : 200,
                'body' : json.dumps("Your email is already verified :)")
            }
    
        elif int(stored_response['Item']['tries']['N']) > 10:
            return{
                'statusCode' : 403,
                'body' : json.dumps("You have exceeded the number of tries, use a different email ID"),
            }
        
        elif current_epochtime > float(stored_response['Item']['epoch_time']['N']) + 600:
            return{
                'statusCode' : 403,
                'body' : json.dumps("The OTP has been expired, retry sending the OTP, time limit before expiry is 10 minutes!")
            }
        
        elif int(stored_response['Item']['OTP']['N']) == unverifiedOTP:
            
            response_dynamo = client_dynamodb.update_item(
                TableName='OTP3_expiry_tries_01',
                Key={
                    'email': {
                        'S': API_email
                    }
                },
                AttributeUpdates = { 
                    "verified_status":{ 
                        "Value": {
                            "BOOL": True,
                            },
                        },
                },
            )
            
            return{
                'statusCode' : 200,
                'body' : """Your OTP is sucessfully verified! 
                    Arabella's got some interstellar-gator skin boots
                    And a Helter Skelter 'round her little finger and I ride it endlessly
                    She's got a Barbarella silver swimsuit
                    And when she needs to shelter from reality she takes a dip in my daydreams
                    My days end best when this sunset gets itself
                    Behind that little lady sitting on the passenger side
                    It's much less picturesque without her catching the light
                    The horizon tries but it's just not as kind on the eyes
                    As Arabella
                    As Arabella
                    Just might have tapped into your mind and soul
                    You can't be sure
                    Arabella's got a seventies head
                    But she's a modern lover
                    It's an exploration, she's made of outer space
                    And her lips are like the galaxy's edge
                    And her kiss the color of a constellation falling into place
                    My days end best when this sunset gets itself
                    Behind that little lady sitting on the passenger side
                    It's much less picturesque without her catching the light
                    The horizon tries but it's just not as kind on the eyes
                    As Arabella
                    As Arabella
                    Just might have tapped into your mind and soul
                    You can't be sure
                    That's magic in a cheetah print coat
                    Just a slip underneath it I hope
                    Asking if I can have one of those
                    Organic cigarettes that she smokes
                    Wraps her lips round the Mexican coke
                    Makes you wish that you were the bottle
                    Takes a sip of your soul and it sounds like.
                    *insert Guitar Solo
                    Just might have tapped into your mind and soul
                    You can't be sure
                    """
            }
            
    else:
        return{
            'statusCode' : 403,
            'body' : json.dumps("You have not requested an OTP yet, pls do that :) ")
        }
    
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
