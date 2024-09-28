import json, boto3

client = boto3.client('dynamodb')

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
    
