from _signal import CTRL_C_EVENT
from _winapi import CREATE_NEW_PROCESS_GROUP

import os
from subprocess import Popen
import requests
import logging

from tests.test_logger import logger
from request_test.request_test import rest_request_test


class TestFunctional(object):
    """Perform basic functional tests using the rest_request_test function against a simple REST API."""

    def setup_method(self):
        """Set up the server for functional tests."""
        logging.debug('Starting flask server')
        os.environ['FLASK_APP'] = 'tests/functional/server.py'
        logger.debug('FLASK_APP is {}'.format(os.getenv('FLASK_APP')))
        self.server = Popen(['flask', 'run'], shell=True, creationflags=CREATE_NEW_PROCESS_GROUP)
        assert self.server is not None

    def test_basic_get(self):
        """Confirm that a simple get against the server works as expected."""
        response = requests.get('http://localhost:5000')
        assert response.status_code == 200
        logger.debug(response)

        assert rest_request_test('http://localhost:5000', requests.get,
                                 expected_response_dict={'Message': 'Hello World!'})

    def teardown_method(self):
        """Shutdown the server and cleanup from tests."""
        # TODO: Find a way to shut down flask without feeding it a Ctrl+C; this feels clunky.
        logger.debug('Shutting down flask server')
        self.server.send_signal(CTRL_C_EVENT)
        logger.info('Server terminated')
