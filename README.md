# CloudFront Logs Parser Lambda OpenSearch

This project is a Serverless application that parses CloudFront logs stored in an S3 bucket and ingests them into an OpenSearch cluster. The application is built using Python and deployed using the Serverless Framework. CI/CD is managed with GitHub Actions.


## Prerequisites

1. Node.js and npm
2. Serverless Framework
3. AWS Account
4. OpenSearch Cluster

## Setup using github actions

### Step1: Fork this repo

Update the serverless.yml with below details
1. desired s3 bucket name and prefix
2. Add requried region

### Step2: Add secrets:
Add the following secrets to your GitHub repository settings:

```bash
MY_AWS_ACCESS_KEY
MY_AWS_SECRET_KEY
OPENSEARCH_HOST
OPENSEARCH_USERNAME
OPENSEARCH_PASSWORD
```

### Step3: Deploy the Application:

Deploy the Serverless application to AWS using [deploy](.github/workflows/deploy.yml) action


## Serverless Configuration
The Serverless configuration is set up to handle S3 events for the specified bucket. It uses the serverless-python-requirements plugin to manage Python dependencies.

Source Code
src/cloudfront_parser.py: Contains the logic to parse CloudFront logs.
src/lambda_handler.py: AWS Lambda handler to process S3 events, parse logs, and ingest into OpenSearch.
src/version.py: Contains version information.

## Testing
To run tests, use the following command:

```bash
pytest
```

## Manual installation 

### Step 1: Package Installation

```bash
git clone git@github.com:malikparvez/cloudfront-logs-parser-lambda-opensearch.git

cd cloudfront-logs-parser-lambda-opensearch
```

Install Python Dependencies:
Ensure you have Python 3.11 installed. Install the necessary Python packages using pip:

```bash
pip3 install --target ./package -r requirements-lambda.txt

cd package

zip -r ../my_deployment_package.zip .

cd ..

cd src

zip -r ../my_deployment_package.zip cloudfront_parser.py lambda_handler.py version.py
```

### Step 2: AWS Lambda Deployment
Upload the generated zip file (my_deployment_package.zip) to AWS Lambda. Set the following environment variables in Lambda:


### Step 3: AWS And OpenSearch Credentials
Set the following AWS and OpenSearch credentials as environment variables:

```
MY_AWS_ACCESS_KEY = ''
MY_AWS_SECRET_KEY = ''
OPENSEARCH_HOST = ''
OPENSEARCH_USERNAME = ''
OPENSEARCH_PASSWORD = ''
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

## Challenges
1. Make sure to have right permissions for the IAM role you have added.

## Contributing
Contributions are welcome! Please create a pull request or open an issue to discuss any changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

