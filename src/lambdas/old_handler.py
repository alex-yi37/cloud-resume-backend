import json, boto3

# need to specify region name in case it can't be inferred from something like
# aws config files (e.g. when using cli client). In AWS console, I imagine region
# name can also be inferred based on account info
# here, though, there isn't anything to infer the region from, so specifying it explicitly

# per this github issue, might want to create the client inside the hanlder instead of outside?
# https://github.com/getmoto/moto/issues/5493#issuecomment-1260138353
# seems like it's possible that if client is created before any mocks from moto, the client would be reaching out to aws
# instead of getting mocked?

# also found this article and repo from aws for creating a lambda handler and associated aws resources
# https://aws.amazon.com/blogs/devops/unit-testing-aws-lambda-with-python-and-mock-aws-services/
# https://github.com/aws-samples/serverless-test-samples/blob/main/python-test-samples/lambda-mock/src/sample_lambda/app.py
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
    
