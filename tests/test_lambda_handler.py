import json
from unittest.mock import patch, MagicMock
from src.lambda_handler import lambda_handler

import pytest

@pytest.fixture
def mock_environment_variables():
    return {
        'aws_access_key': 'fake_access_key',
        'aws_secret_key': 'fake_secret_key',
        'opensearch_host': 'fake_host',
        'opensearch_username': 'fake_username',
        'opensearch_password': 'fake_password',
        'aws_access_key': 'fake_access',
        'aws_secret_key': 'fake_secret',
    }

@pytest.fixture
def event():
    return {
        'Records': [{
            's3': {
                'bucket': {'name': 'test_bucket'},
                'object': {'key': 'test_key.gz'}
            }
        }]
    }

@pytest.fixture
def context():
    return {}

# Add happy path test

# def test_lambda_handler_success(event, context, mock_environment_variables):
#     with patch.dict('os.environ', mock_environment_variables):
#         with patch('src.lambda_handler.boto3.client') as mock_s3_client:
#             with patch('src.lambda_handler.OpenSearch') as mock_opensearch:
#                 mock_s3_client.return_value.get_object.return_value = {"Body": MagicMock()}
#                 mock_opensearch.return_value.bulk.return_value = None
#                 result = lambda_handler(event, None)
#                 assert result['statusCode'] == 200
#                 assert 'CloudFront logs ingested into OpenSearch successfully!' in result['body']

def test_lambda_handler_missing_environment_variables(event, context):
    with patch.dict('os.environ', {}):
        result = lambda_handler(event, context)
        
        assert result['statusCode'] == 500



