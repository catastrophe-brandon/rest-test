import logging
import os
from subprocess import Popen

import requests
import psutil

from request_test.request_test import rest_request_test
from tests.logger_config import logger


class TestFunctional(object):
    """Perform basic functional tests using the rest_request_test function against a simple REST API."""

    def setup_class(cls):
        """Start flask server once for this class."""
        logging.debug('Starting flask server')
        os.environ['FLASK_APP'] = 'tests/functional/server.py'
        logger.debug('FLASK_APP is {}'.format(os.getenv('FLASK_APP')))
        cls.server = Popen(['flask', 'run'], shell=True)
        assert cls.server.returncode is None
        assert cls.server is not None

    def teardown_class(cls):
        """Shutdown the server and cleanup from tests."""
        # TODO: Find a way to shut down flask without feeding it a Ctrl+C; this feels clunky.
        logger.debug('Shutting down flask server')
        server_process = psutil.Process(pid=cls.server.pid)
        server_process.kill()
        logger.info('Server terminated')

    def setup_method(self):
        """Set up instance specific test stuff."""
        logging.debug('Test setup called.')
        self.url = 'http://localhost:5000'

    def teardown_method(self):
        """Tear down for individual test instance."""
        logging.debug('Test teardown called.')

    def test_basic_get(self):
        """Confirm that a simple get against the server works as expected."""
        response = requests.get(self.url)
        assert response.status_code == 200
        logger.debug(response)

        assert rest_request_test(self.url, requests.get,
                                 expected_response_dict={'Message': 'Hello World!'})

    def test_basic_put(self):
        """Confirm that a simple PUT against the server works as expected."""
        pass

    def test_basic_post(self):
        """Confirm that a simple POST against the server works as expected."""
        pass

    def test_basic_delete(self):
        """Confirm that a simple DELETE against the server works as expected."""
        assert rest_request_test(self.url + '/delete/404', requests.delete, expected_status=404)
        assert rest_request_test(self.url + '/delete/204', requests.delete, expected_status=204)

    def test_disallowed_methods(self):
        """Confirm that attempting disallowed methods returns a 405."""
        assert rest_request_test(self.url, requests.post, expected_status=405)
        assert rest_request_test(self.url, requests.put, expected_status=405)
        assert rest_request_test(self.url, requests.patch, expected_status=405)
        assert rest_request_test(self.url, requests.delete, expected_status=405)
