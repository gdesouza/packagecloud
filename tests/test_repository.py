"""
test_repository.py

MIT License
Copyright (c) 2020 Gustavo de Souza
Author: Gus de Souza
"""

import unittest
import logging
import json

from repository import RepositoryClient
from api_token import load_token


class TestMethods(unittest.TestCase):
    """Unit tests for repository class"""

    def setUp(self):

        user = 'avidbots'
        repo = 'ros-noetic'
        distro = 'ubuntu'
        api_token = load_token()

        self.repo = RepositoryClient(user, repo, distro, api_token)

        self.assertEqual(self.repo.user, user)
        self.assertEqual(self.repo.repo, repo)
        self.assertEqual(self.repo.distro, distro)
        self.assertEqual(self.repo.api_token, api_token)
        self.assertEqual(self.repo.domain_base,
                         f"{self.repo.http_scheme}://{self.repo.api_token}:@{self.repo.api_domain}")
        self.assertEqual(self.repo.url_base,
                         f"{self.repo.domain_base}/api/{self.repo.api_version}")

    @unittest.skip
    def test_repo_get_packages(self):
        """Test Get packages"""

        packages = self.repo.get_packages()
        self.assertNotEqual(len(packages), 0)
        logging.debug(json.dumps(packages))

    @unittest.skip
    def test_repo_get_packages_error(self):
        """Test get packages with invalid repository"""

        self.repo.repo = 'asdf'
        packages = self.repo.get_packages()
        self.assertEqual(len(packages), 0)
        logging.debug(json.dumps(packages))

    @unittest.skip
    def test_get_number_packages(self):
        """Get number of packages with success"""

        self.repo.repo = 'live'
        number = self.repo.get_number_of_packages()
        self.assertNotEqual(0, number)

    # def test_load_token(self):
    #     token = 'test_token'
    #     pkgcloud = Packagecloud(token)
    #     self.assertEqual(pkgcloud.token, token)
    #     self.assertIn(token, pkgcloud.url)

    # def test_get_total_packages(self):
    #     pkgcloud = Packagecloud()

    #     total = pkgcloud.get_total_packages(self.repo)
    #     self.assertNotEqual(total, 0)

    #     print(f'{self.repo} contains {total} packages')

    #     total = pkgcloud.get_total_packages('invalid_repo')
    #     self.assertEqual(total, 0)

    # def test_get_all_packages(self):
    #     pkgcloud = Packagecloud()

    #     total = pkgcloud.get_total_packages(self.repo)
    #     packages = pkgcloud.get_all_packages(self.repo)

    #     self.assertEqual(len(packages), total,
    #          'Number of retrieved versions should be the total number of versions')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
