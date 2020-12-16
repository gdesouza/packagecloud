#!/usr/bin/env python3

import requests
import json
import unittest
import os
import re


class Packagecloud:
    """Interface class to use packagecloud.io API
    """

    def __init__(self, token=None):
        """Initialize class with token"""

        if token:
            self.set_token(token)
        else:
            self.load_token()


    def set_token(self, token):
        """Set token and update URL"""

        self.token = token
        self.url = f'https://{token}:@packagecloud.io'



    def load_token(self):
        '''Load packagecloud token
        
        Try to use env var PACKAGECLOUD_API_KEY first (for jenkins jobs)
        If it is not set then try to read it from ~/.packagecloud 
        '''

        token = ''
        
        if(os.environ.get("PACKAGECLOUD_API_KEY")):
            token = os.environ.get("PACKAGECLOUD_API_KEY")

        else:

            PACKAGE_CLOUD_FILE = ".packagecloud"
            home = os.path.expanduser("~")

            cfg_file_path = os.path.join(home, PACKAGE_CLOUD_FILE)

            try:
                with open(cfg_file_path, "r") as cfg_file:
                    cfg_file_content = cfg_file.read()
                
                token = json.loads(cfg_file_content)["token"]

            except FileNotFoundError:
                print_err("Error: Failed to obtain package cloud token from %s" % cfg_file_path)
                token = ''

            
        self.set_token(token)


    def get_request(self, action, parms):
        """Make GET request to packagecloud API
        """

        url = f'{self.url}/{action}'
        if parms:
            url += f'?{self.json_to_url_params(parms)}'

        # print(f'Request: {url}')
        return requests.get(url, timeout=120)




    def get_request_paged(self, action, parms, page):
        """Make GET request to packagecloud API
        """

        url = f'{self.url}/{action}?page={page}'
        if parms:
            url += f'&{self.json_to_url_params(parms)}'

        # print(f'Request: {url}')
        return requests.get(url, timeout=120)




    def delete_request(self, action):
        """Make DELETE request to packagecloud API"""
        
        url = f'{self.url}/{action}'
        return requests.delete(url, timeout=120)



    def json_to_url_params(self, params):
        list_params = []
        for key in params:
            value = params[key]
            list_params.append(f'{key}={value}')
        return '&'.join(list_params)


    
    def search_packages(self, repo, filter):
        """Search for packages that match a filter"""

        parms = {
            'q': f'{filter}',
            'dist': 'ubuntu'
        }

        cmd = f'/api/v1/repos/avidbots/{repo}/search'
        return self.get_objects(cmd, parms)


    def search_packages_regex(self, repo, regex):
        """Search for packages that match a regular expression
        
        Packagecloud doesn't provide a way to filter using regular 
        expressions. This method gets all the packages and filters
        the results based on the given regular expression.

        Args:
            repo: The repository 
            regex: The regular expression
        """
        
        all_packages = self.get_all_packages(repo)
        matched_packages = []

        for package in all_packages:
            regex = re.compile(regex)

            match_name = regex.fullmatch(package["name"])
            match_version = regex.fullmatch(package["version"])

            if match_name or match_version:
                matched_packages.append(package)

        return matched_packages



    def get_versions(self, repo, package_name):
        """Get versions of a given package on a specific repo"""

        cmd = f'/api/v1/repos/avidbots/{repo}/package/deb/ubuntu/xenial/{package_name}/amd64/versions.json'
        return self.get_objects(cmd)



    def get_all_packages(self, repo):
        """Get all packages from a given repo"""

        cmd = f'/api/v1/repos/avidbots/{repo}/packages.json'
        return self.get_objects(cmd)



    def get_objects(self, cmd, parms=None):
        """Get objects from packagecloud according to the given command"""

        page = 1
        objects = []
        total_num_objects = 0

        response = self.get_request(cmd, parms)

        # if not 200 OK
        if not response.ok:
            print(f'ERROR: HTTP return code: {response.status_code} ({cmd})')
            return objects

        # always use the total number of packages returned by first 
        # request as the reference
        objects += response.json()

        total = int(response.headers["Total"])
        read = len(objects)

        # print(f'Reading {read} of {total}')

        while read < total:
            page += 1
            response = self.get_request_paged(cmd, parms, page)

            # if not 200 OK
            if not response.ok:
                break

            objects += response.json()
            read = len(objects)

            # print(f'Reading {read} of {total}')

        # sanity check, since multiple requests are made. We might have race
        # conditions. Inform user if there are anything strange going on
        if len(objects) != total:
            print('WARNING: Number of retrieved objects does not match ' +
                   f'({len(objects)} retrieved, should be {total})' )

        return objects



    def delete_packages(self, packages):
        """Delete packages from packagecloud
        
        Args:
            packages: list of packages. Each item is a JSON object containing
                      the following elements:
            {
                "filename": "jakedotrb-0.0.1.gem",
                "destroy_url": "/api/v1/repos/test_user/test_repo/gems/jakedotrb-0.0.1.gem"
            }
                        
        """

        for package in packages:
            cmd = package['destroy_url']
            name = package['filename']

            request = delete_request(cmd)

            if request.status_code != 200:
                print(f'ERROR: HTTP return code: {request.status_code} ({cmd})')
            else:
                print(f'Successfully deleted {name}!')


    def print_packages(self, packages):
        for package in packages:
            name = package['name'] 
            version = package['version']
            release = package['release']
            print(f'{name}_{version}-{release}')


    def list_versions(self, repo, package_name):
        self.print_packages(self.get_versions(repo, package_name))


    def list_packages(self, repo):
        self.print_packages(self.get_all_packages(repo))


    def get_total_packages(self, repo):
        """Make GET request to packagecloud API
        """

        cmd = f'/api/v1/repos/avidbots/{repo}/packages.json'
        url = f'{self.url}/{cmd}?per_page=0'
        
        response = requests.get(url, timeout=120)
        
        if response.ok:
            return int(response.headers['Total'])
        else:
            return 0




###############################################################################
# Unit tests
###############################################################################


class TestMethods(unittest.TestCase):
    """Unit tests for Packagecloud class

    """
    
    def setUp(self):
        self.repo = 'live'


    def test_load_token(self):
        token = 'test_token'
        pkgcloud = Packagecloud(token)
        self.assertEqual(pkgcloud.token, token)
        self.assertIn(token, pkgcloud.url)

    def test_get_total_packages(self):
        pkgcloud = Packagecloud()

        total = pkgcloud.get_total_packages(self.repo)
        self.assertNotEqual(total, 0)

        print(f'{self.repo} contains {total} packages')


        total = pkgcloud.get_total_packages('invalid_repo')
        self.assertEqual(total, 0)


    def test_get_all_packages(self):
        pkgcloud = Packagecloud()

        total = pkgcloud.get_total_packages(self.repo)
        packages = pkgcloud.get_all_packages(self.repo)

        self.assertEqual(len(packages), total, 
             'Number of retrieved versions should be the total number of versions')






if __name__ == '__main__':
    unittest.main()
