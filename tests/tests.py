import json
from unittest.mock import patch

from request_test.request_test import rest_request_test

good_test_post_url = ''
good_test_get_url = 'http://www.google.com'


def test_post():
    """Test a post request."""
    pass


@patch('request_test.request_test.requests.get')
def test_get(mock_get):
    """Test a get request."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = json.dumps({'potato': '12345'})
    assert rest_request_test(good_test_get_url, mock_get, None, None, 200, expected_response_dict={'potato': '12345'})


def test_put():
    """Test a put request."""
    pass


def test_options():
    """Test an options request."""
    pass
