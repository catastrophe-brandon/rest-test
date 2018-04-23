import json
from unittest.mock import patch

import pytest

from request_test.request_test import rest_request_test

good_test_post_url = 'http://127.0.0.1'
good_test_get_url = 'http://www.google.com'


@patch('request_test.request_test.requests.post')
def test_post(mock_post):
    """Test a post request."""
    mock_post.return_value.status_code = 201
    mock_post.return_value.content = json.dumps({'Message': 'Created'})
    body_dict = {'potatoes': 1}
    headers_dict = {'tomaters': 2}
    assert rest_request_test(good_test_post_url, mock_post, body_dict, headers_dict, expected_status=201,
                             expected_response_dict={'Message': 'Created'})

    with pytest.raises(AssertionError):
        rest_request_test(good_test_post_url, mock_post, body_dict, headers_dict, expected_status=485,
                          expected_response_dict={'Message': 'Created'})

    with pytest.raises(AssertionError):
        rest_request_test(good_test_post_url, mock_post, body_dict, headers_dict, expected_status=485,
                          expected_response_dict={'Message': 'Cratered'})


@patch('request_test.request_test.requests.get')
def test_get(mock_get):
    """Test a get request."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = json.dumps({'potato': '12345'})
    assert rest_request_test(good_test_get_url, mock_get, None, None, 200, expected_response_dict={'potato': '12345'})


def test_put():
    """Test a put request."""
    # TODO:
    pass


@patch('request_test.request_test.requests.options')
def test_options(mock_options):
    """Test an options request."""
    mock_options.return_value.status_code = 200
    mock_options.return_value.content = json.dumps({'Allow': 'HEAD,GET,PUT,DELETE,OPTIONS'})
    assert rest_request_test(good_test_get_url, mock_options, None, None, 200,
                             expected_response_dict={'Allow': 'HEAD,GET,PUT,DELETE,OPTIONS'})


@patch('request_test.request_test.requests.delete')
def test_delete(mock_delete):
    """Test a delete operation."""
    mock_delete.return_value.status_code = 204
    mock_delete.return_value.content = None
    assert rest_request_test('http://127.0.0.1/poopy/pants', mock_delete, None, None, 204, expected_response_dict=None)
