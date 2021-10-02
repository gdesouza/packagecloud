"""
test_packagecloud.py

MIT License
Copyright (c) 2020 Gustavo de Souza
Author: Gus de Souza
"""

import unittest
import logging

from baseclient import BasePackageCloudClient


class TestMethods(unittest.TestCase):
    """Unit tests for Packagecloud class"""

    def test_init(self):
        """Test class initialization"""

        api_token = 'SOMETOKEN'
        http_scheme = 'https'
        api_domain = 'packagecloud.io'
        api_version = 'v1'

        client = BasePackageCloudClient(api_token, http_scheme, api_domain, api_version)

        self.assertEqual(api_token, client.api_token)
        self.assertEqual(http_scheme, client.http_scheme)
        self.assertEqual(api_domain, client.api_domain)
        self.assertEqual(api_version, client.api_version)
        self.assertEqual(client.domain_base, f'{http_scheme}://{api_token}:@{api_domain}')
        self.assertEqual(client.url_base, f'{client.domain_base}/api/{api_version}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    unittest.main()
