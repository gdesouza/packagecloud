"""
test_token.py

MIT License
Copyright (c) 2020 Gustavo de Souza
Author: Gus de Souza
"""

import unittest
import os
import random
import logging

from api_token import read_token_from_env, read_token_from_file


class TestToken(unittest.TestCase):
    """Unit tests for api_token class"""

    def setUp(self):
        self.temp_files = []

    def tearDown(self):
        for temp_file in self.temp_files:
            os.remove(temp_file)

    def temp_file(self):
        """Creates and empty file and returns it's path"""

        temp_file_name = f"/tmp/test_token_{random.randint(1,1000)}.tmp"
        open(temp_file_name, 'a').close()

        self.temp_files.append(temp_file_name)
        return temp_file_name

    def test_read_token_from_env_fail(self):
        """Read token but environment variable is not set"""

        old_value = os.environ.get('PACKAGECLOUD_API_KEY', '')
        os.environ.pop('PACKAGECLOUD_API_KEY', None)

        result = read_token_from_env()
        self.assertEqual(result, '')

        os.environ['PACKAGECLOUD_API_KEY'] = old_value

    def test_read_token_from_env(self):
        """Read token from existing environment variable"""

        old_value = os.environ.get('PACKAGECLOUD_API_KEY', '')
        expected = 'abcdefgh'
        os.environ['PACKAGECLOUD_API_KEY'] = expected

        result = read_token_from_env()
        self.assertEqual(result, expected)
        os.environ['PACKAGECLOUD_API_KEY'] = old_value

    def test_read_token_from_file_fail(self):
        """Read token from non existing file"""

        result = read_token_from_file('/some/non/existent/file')
        self.assertEqual(result, '')

    def test_parse_error_read_token(self):
        """Read token from file fails parsing"""

        temp_file = self.temp_file()

        result = read_token_from_file(temp_file)
        self.assertEqual(result, '')

    def test_read_token_file(self):
        """Read token from file succeeds"""

        temp_file = self.temp_file()
        with open(temp_file, "a") as file:
            file.write("token: 'abcdefgh'")

        result = read_token_from_file(temp_file)
        self.assertEqual(result, '')


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    unittest.main()
