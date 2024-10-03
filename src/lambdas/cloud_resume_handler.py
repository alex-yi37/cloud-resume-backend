import json, boto3
from os import environ

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

_LAMBDA_DYNAMO_DB_CLIENT = {
    "client": boto3.client("dynamodb", region_name = environ.get("AWS_REGION", "us-east-1")),
    "table_name": environ.get("DYNAMO_DB_TABLE_NAME", "NONE"),
    "primary_key_value": environ.get("DYNAMO_DB_PK_VALUE", "NONE")
}

class DynamoDBClass:
    def __init__(self, lambda_dynamo_db_client):
        self.client = lambda_dynamo_db_client["client"]
        self.table_name = lambda_dynamo_db_client["table_name"]
        self.primary_key_value = lambda_dynamo_db_client["primary_key_value"]

def lambda_handler(event, context):
    global _LAMBDA_DYNAMO_DB_CLIENT

    dynamodb_client_class = DynamoDBClass(_LAMBDA_DYNAMO_DB_CLIENT)

    try:
        response = dynamodb_client_class.client.update_item(
            TableName=dynamodb_client_class.table_name,
            # wanted to set the 'site_name' in the 'Key' arg dynamically, but seems like I would have to loop to do that
            # so I'm not going to bother and instead just hard code 'site_name' 
            Key = {
                'site_name': {'S': dynamodb_client_class.primary_key_value}
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
    
