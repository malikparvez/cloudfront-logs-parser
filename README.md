# CloudFront Logs Parser Lambda for OpenSearch

This repository contains code to parse CloudFront logs from an S3 bucket and send the parsed data to OpenSearch.

## How to Use

### Step 1: Package Installation

```bash
mkdir package
pip3 install --target ./package opensearch-py
cd package
zip -r ../my_deployment_package.zip .
cd ..
zip my_deployment_package.zip lambda_function.py
```

### Step 2: AWS Lambda Deployment
Upload the generated zip file (my_deployment_package.zip) to AWS Lambda. Set the following environment variables in Lambda:


### Step 3: AWS And OpenSearch Credentials
Set the following AWS and OpenSearch credentials as environment variables:

```
aws_access_key = ''
aws_secret_key = ''
opensearch_host = ''
opensearch_username = ''
opensearch_password = ''
```

### Step 4: Set Up S3 Event Trigger
To automatically trigger the Lambda function when new CloudFront logs are added to your S3 bucket, follow these steps:

1. Navigate to the AWS S3 console.
2. Select the S3 bucket containing your CloudFront logs.
3. Go to the "Properties" tab and click on "Events."
4. Add a new event configuration with the following settings:
5. Event Name: Choose a descriptive name (e.g., "CloudFrontLogsEvent").
6. Events: Select "PUT" event
7. Prefix: (Optional) Specify a prefix if your CloudFront logs are stored in a specific folder within the bucket.
8. Suffix: (Optional) Specify a suffix if your CloudFront logs have a specific file extension.
9. Click "Add" to save the configuration.
    
Now, whenever new CloudFront logs are added to the specified S3 bucket, the Lambda function will be automatically triggered to parse and send the data to OpenSearch.
