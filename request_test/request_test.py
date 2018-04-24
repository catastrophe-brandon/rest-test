import json
import logging

import requests

logger = logging.getLogger(__name__)


def rest_request_test(request_url, request_type, request_body_dict=None, request_headers_dict=None, expected_status=200,
                      expected_response_dict=None, verify=True, timeout=3):
    """
    Issue a request of the specified type against the specified URL, and provided the specified header/body data.

    Confirm the specified expected status value and expected response data match the response from the endpoint.

    :param request_url
    :param request_type function reference to requests.post, requests.put, requests.patch, requests.delete, etc.
    :param request_body_dict
    :param request_headers_dict
    :param expected_status
    :param expected_response_dict
    :param verify should be set to True if SSL certificate verification is desired.
    :param timeout
    """
    assert request_url is not None and request_url != '', 'request_url is a required parameter'

    if request_body_dict is not None:
        assert type(request_body_dict) == dict, 'request_body data needs to be provided as a dict'

    if request_headers_dict is not None:
        assert type(request_headers_dict) == dict, 'request_headers data needs to be provided as a dict'

    # invoke the request function
    if request_type == requests.delete or request_type == requests.options:
        response = request_type(request_url, verify=verify, timeout=timeout)
    else:
        response = request_type(request_url, headers=request_headers_dict, json=request_body_dict, verify=verify,
                                timeout=timeout)

    logger.debug('Response status code: %d' % response.status_code)
    assert expected_status == response.status_code,\
        'Expected {} but got {}'.format(expected_status, response.status_code)

    if expected_response_dict is not None:
        assert expected_response_dict == json.loads(response.content), \
            'mismatch between expected response and actual response content'
    else:
        logger.debug('Expected response not given; not inspecting response content')

    return True
