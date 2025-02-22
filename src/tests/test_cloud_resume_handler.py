import unittest
import os
import boto3
import json
from moto import mock_aws

# maybe try this from moto documentation for using unittest?
# https://docs.getmoto.org/en/stable/docs/getting_started.html#unittest-usage
@mock_aws
class TestLambdaHandler(unittest.TestCase):
    def setUp(self):
      """Mocked AWS Credentials for moto."""
      os.environ["AWS_ACCESS_KEY_ID"] = "testing"
      os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
      os.environ["AWS_SECURITY_TOKEN"] = "testing"
      os.environ["AWS_SESSION_TOKEN"] = "testing"
      os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

      dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

      table = dynamodb.create_table(
        TableName = "WebsiteViewCount",
        KeySchema=[{"AttributeName": "site_name", "KeyType": "HASH"}],
        AttributeDefinitions=[
           {
            "AttributeName": "site_name", 
            "AttributeType": "S"
           },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        # Note: got the following error: "An error occurred (ValidationException) when calling 
        # the CreateTable operation: ProvisionedThroughput cannot be specified when BillingMode is PAY_PER_REQUEST
        # when BillingMode attribute is set
        # BillingMode='PAY_PER_REQUEST'"
      )

      test_item = {
         "site_name": "asd",
         "view_count": 0
      }

      table.put_item(Item=test_item)

    def test_lambda_handler_response(self):
      from ..lambdas import cloud_resume_handler

      response = cloud_resume_handler.lambda_handler({}, {})

      # read response body as json and turn it into a dict
      body = json.loads(response["body"])

      self.assertEqual(response["statusCode"], 200)
      self.assertEqual(body["data"]["viewCount"], 1)
      
    
