import logging
import os
from subprocess import Popen

import requests
import psutil
import socket
import time

from request_test.request_test import rest_request_test
from tests.logger_config import logger


def kill_all(process_name):
    """Kill all processes with the name matching process_name."""
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            logging.debug('Killing process {} with name {}'.format(proc.pid, process_name))
            proc.kill()


def is_open(port_number):
    """Return True if a port is open."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex(('127.0.0.1', port_number))
    s.close()
    if result == 0:
        return True
    else:
        return False


class TestFunctional(object):
    """Perform basic functional tests using the rest_request_test function against a simple REST API."""

    def setup_class(cls):
        """Start flask server once for this class."""
        kill_all('flask')
        kill_all('flask.exe')
        time.sleep(2)
        logging.debug('Starting flask server')
        assert os.getenv('FLASK_APP') is not None
        logger.debug('FLASK_APP is {}'.format(os.getenv('FLASK_APP')))
        logger.debug('SERVER_NAME is {}'.format(os.getenv('SERVER_NAME')))
        cls.server = Popen(['flask', 'run'])
        logger.debug('flask process pid is {}'.format(cls.server.pid))
        assert cls.server.returncode is None
        time.sleep(2)
        assert is_open(5000)
        cls.server.poll()
        assert cls.server.returncode is None

    def teardown_class(cls):
        """Shutdown the server and cleanup from tests."""
        logger.debug('Shutting down flask server')
        kill_all('flask.exe')
        kill_all('flask')
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
