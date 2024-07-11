import gzip
import io
from datetime import datetime
from src.cloudfront_parser import parse_cloudfront_logs

import pytest

@pytest.fixture(scope="module")
def sample_log_file_path():
    return "tests/fixtures/sample_cloudfront_logs.gz"

def test_parse_cloudfront_logs(sample_log_file_path):
    with gzip.open(sample_log_file_path, 'rb') as f:
        logs = parse_cloudfront_logs(f)
    
    assert logs[1]['x-edge-location'] == 'ATL56-C2'
    assert logs[1]['cs-method'] == 'GET'
    assert logs[1]['cs-uri-stem'] == '/api/auth/user'
    assert logs[1]['sc-bytes'] == 252
