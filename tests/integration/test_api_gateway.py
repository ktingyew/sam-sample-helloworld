import os

import boto3
import pytest
import requests

"""
Make sure env variable DEV_STACK_NAME exists with the name of the stack we are going to test. 
"""


class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from Cloudformation Stack outputs """
        stack_name = os.environ.get("DEV_STACK_NAME")
        region = os.environ.get("AWS_REGION")
        cloudformation_role_arn = os.environ.get("DEV_CLOUDFORMATION_EXECUTION_ROLE")
        cred_profile = os.environ.get("AWS_CREDENTIALS_PROFILE")

        if stack_name is None:
            raise ValueError('Please set the DEV_STACK_NAME environment variable to the name of your stack')

        if cred_profile is None:
            sts_client = boto3.client('sts')
        else:
            session = boto3.session.Session(profile_name=cred_profile)
            sts_client = session.client('sts')

        # Call the assume_role method of the STSConnection object and pass the role
        # ARN and a role session name.
        assumed_role_object=sts_client.assume_role(
            RoleArn=cloudformation_role_arn,
            RoleSessionName="AssumeRoleSession1"
        )

        # From the response that contains the assumed role, get the temporary 
        # credentials that can be used to make subsequent API calls
        credentials=assumed_role_object['Credentials']

        client = boto3.client(
            "cloudformation", 
            region_name=region,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n" f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "HelloWorldApi"]

        if not api_outputs:
            raise KeyError(f"HelloWorldAPI not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extract url from stack outputs

    def test_api_gateway(self, api_gateway_url):
        """ Call the API Gateway endpoint and check the response """
        response = requests.get(api_gateway_url)

        assert response.status_code == 200
        assert response.json() == {"message": "hello world"}
