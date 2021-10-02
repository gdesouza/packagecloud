"""
test_request.py

MIT License
Copyright (c) 2020 Gustavo de Souza
Author: Gus de Souza
"""

# Standard library
import unittest
from unittest.mock import patch
import logging

# Internal
from request import Request


class TestRequest(unittest.TestCase):
    """Unit tests for request class"""

    @classmethod
    def setUpClass(cls):
        cls.mock_get_patcher = patch('requests.get')
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.mock_get_patcher.stop()

    def test_init(self):
        """Test class initialization"""

        self.mock_get.return_value.ok = True

        url = "http"
        timeout = 120
        request = Request(url, timeout)
        response = request.get('repo')
        self.assertIsNotNone(response)


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    unittest.main()
