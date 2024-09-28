import json, boto3

# need to specify region name in case it can't be inferred from something like
# aws config files (e.g. when using cli client). In AWS console, I imagine region
# name can also be inferred based on account info
# here, though, there isn't anything to infer the region from, so specifying it explicitly
client = boto3.client('dynamodb', region_name = "us-east-1")

def lambda_handler(event, context):
    try:
        response = client.update_item(
            TableName='WebsiteViewCount',
            Key = {
                'site_name': {'S': 'cloud_resume_challenge'}
            },
            # could also use 'SET view_count = view_count + :inc' as the update expression
            UpdateExpression = 'ADD view_count :inc',
            ExpressionAttributeValues = {":inc" : {"N": "1"}},
            ReturnValues = 'UPDATED_NEW'
        )
        
        retrieved_count = response["Attributes"]["view_count"]["N"]
        
        data = json.dumps({
                'data': {
                    'viewCount': int(retrieved_count)
                }
            }
        )
        
        
        return {
            'statusCode': 200,
            'headers': {
                'content-type': 'application/json',
            },
            'body': data
        }
    except Exception as err:
        err_response = json.dumps({
            'error': {
                'message': str(err)
            }
        })
        
        return {
            'statusCode': 500,
            'headers': {
                'content-type': 'application/json',
            },
            'body': err_response
        }
    
