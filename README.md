# sam-with-cicd-repo

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. 

## Initialisation

Create the following:
- A S3 bucket for storing artifacts
- A new AWS User with credential keys
  - Can have no permissions
- A AWS Role for GitHub Actions
  - Allow `sts:AssumeRole` for the User
- A AWS Role for CloudFormation service

You can use `sam pipeline bootstrap` to create the above (except the User) automatically.

## Files

- .github/workflows - CI/CD workflow via GitHub Actions.
- hello_world - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- tests - Unit and integration tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name sam-with-cicd-repo
```

