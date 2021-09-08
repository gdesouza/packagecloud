import unittest
from packagecloud import Repository
from api_token import load_token
import logging
import json

logging.basicConfig(level=logging.CRITICAL)


class TestMethods(unittest.TestCase):
    """Unit tests for Packagecloud class
    """
    
    def setUp(self):
        # user = 'username'
        # repo = 'test'
        # distro = 'ubuntu'
        # api_token = 'abcdefgh'

        user = 'avidbots'
        repo = 'ros-noetic'
        distro = 'ubuntu'
        api_token = load_token()

        self.repo = Repository(user, repo, distro, api_token)

        self.assertEqual(self.repo.user, user)
        self.assertEqual(self.repo.repo, repo)
        self.assertEqual(self.repo.distro, distro)
        self.assertEqual(self.repo.api_token, api_token)
        self.assertEqual(self.repo.domain_base, 
                         f"{self.repo.http_scheme}://{self.repo.api_token}:@{self.repo.api_domain}")
        self.assertEqual(self.repo.url_base, 
                         f"{self.repo.domain_base}/api/{self.repo.api_version}")

    def test_repo_get_packages(self):
        packages = self.repo.get_packages()
        self.assertNotEqual(len(packages), 0)
        logging.debug(json.dumps(packages))

    def test_repo_get_packages_error(self):
        self.repo.repo = 'asdf'
        packages = self.repo.get_packages()
        self.assertEqual(len(packages), 0)
        logging.debug(json.dumps(packages))


    def test_json_to_url_params(self):
        from packagecloud import json_to_url_params
        json_object = {'one':1, 'two':2, 'three': 3}
        url_params = json_to_url_params(json_object)
        self.assertEqual(url_params, "one=1&two=2&three=3")


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
    unittest.main()