import json
import boto3
import os
import urllib.parse
import gzip
from opensearchpy import OpenSearch
from src.cloudfront_parser import parse_cloudfront_logs

def lambda_handler(event, context):
    try:
        # AWS credentials from env variables
        aws_access_key = os.environ['my_aws_access_key']
        aws_secret_key = os.environ['my_aws_secret_key']

        # OpenSearch credentials from env variables
        opensearch_host = os.environ['opensearch_host']
        opensearch_username = os.environ['opensearch_username']
        opensearch_password = os.environ['opensearch_password']


        # Get the S3 bucket and key from the S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

        # Initialize S3 client
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

        opensearch = OpenSearch(
            hosts=[{'host': opensearch_host, 'port': 443}],
            http_auth=(opensearch_username, opensearch_password),
            scheme="https",
            timeout=30, 
            max_retries=3, 
            retry_on_timeout=True
        )

        try:
            object = s3_client.get_object(Bucket=bucket, Key=key)["Body"]
            batch_size = 2000
            with gzip.open(object) as log_file:
                log_data = parse_cloudfront_logs(log_file)
                
                # Loop through the array in batches of 2000
                for i in range(0, len(log_data), batch_size):
                    batch = log_data[i:i + batch_size]
                    opensearch.bulk(body=batch)
                       

        except Exception as e:
         return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {e}')
        }


        return {
            'statusCode': 200,
            'body': json.dumps(f'CloudFront logs for ingested into OpenSearch successfully!')
        }

    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {e}')
        }
