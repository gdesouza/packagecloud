#!/usr/bin/env python3
import requests
import logging


def json_to_url_params(params):
    return '&'.join([
        f'{key}={params[key]}'
        for key in params
    ])


class Request:

    def __init__(self, url, timeout=120):
        self.url = url
        self.timeout = timeout

    def _get_request(self, path, params, page=1):
        """Internal _get_request"""

        url = f'{self.url}/{path}?page={page}'
        if params:
            url += f'&{self.json_to_url_params(params)}'

        # print(f'Request: {url}')
        return requests.get(url, self.timeout)
        

    def get(self, path, params=None):
        """Make GET request to API"""

        page = 1
        objects = []
        total_num_objects = 0

        response = self._get_request(path, params)

        # if not 200 OK
        if not response.ok:
            logging.error(f'ERROR: HTTP return code: {response.status_code} ({path})')
            return objects

        # always use the total number of packages returned by first 
        # request as the reference
        objects += response.json()

        total = int(response.headers["Total"])
        read = len(objects)

        # print(f'Reading {read} of {total}')

        while read < total:
            page += 1
            response = self._get_request(path, params, page)

            # if not 200 OK
            if not response.ok:
                break

            objects += response.json()
            read = len(objects)

            # print(f'Reading {read} of {total}')

        # sanity check, since multiple requests are made. We might have race
        # conditions. Inform user if there are anything strange going on
        if len(objects) != total:
            logging.warning('Number of retrieved objects does not match ' +
                   f'({len(objects)} retrieved, should be {total})' )

        return objects

class Packagecloud:
    """Interface class to use packagecloud.io API"""

    def __init__(self,
                 api_token,
                 http_scheme='https', 
                 api_domain='packagecloud.io', 
                 api_version='v1'):
        self.http_scheme = http_scheme
        self.api_domain = api_domain
        self.api_version = api_version        
        self.api_token = api_token

    @property
    def domain_base(self):
        return f'{self.http_scheme}://{self.api_token}:@{self.api_domain}'

    @property
    def url_base(self):
        return f'{self.domain_base}/api/{self.api_version}'


class Repository(Packagecloud):
    """Repository settings class"""

    def __init__(self, user, repo, distro, api_token):
        super().__init__(api_token)
        self.user = user
        self.repo = repo
        self.distro = distro

    @property
    def path(self):
        return f'repos/{self.user}/{self.repo}/packages.json'

    def get_packages(self):
        """Get all packages from a given repo"""

        return Request(self.url_base).get(self.path)


    # def get(self, path, parms, page=1):
    #     """Make GET request to packagecloud API
    #     """

    #     url = f'{self.url_base}/{path}?page={page}'
    #     if parms:
    #         url += f'&{self.json_to_url_params(parms)}'

    #     # print(f'Request: {url}')
    #     return requests.get(url, timeout=120)



    # def delete_request(self, path):
    #     """Make DELETE request to packagecloud API"""
        
    #     return requests.delete(f'{self.url_base}/{path}', timeout=120)


    
    # def search_packages(self, repo, filter):
    #     """Search for packages that match a filter"""

    #     parms = {
    #         'q': f'{filter}',
    #         'dist': 'ubuntu'
    #     }

    #     cmd = f'/api/v1/repos/avidbots/{repo}/search'
    #     return self.get_objects(cmd, parms)


    # def search_packages_regex(self, repo, regex):
    #     """Search for packages that match a regular expression
        
    #     Packagecloud doesn't provide a way to filter using regular 
    #     expressions. This method gets all the packages and filters
    #     the results based on the given regular expression.

    #     Args:
    #         repo: The repository 
    #         regex: The regular expression
    #     """
        
    #     all_packages = self.get_all_packages(repo)
    #     matched_packages = []

    #     for package in all_packages:
    #         regex = re.compile(regex)

    #         match_name = regex.fullmatch(package["name"])
    #         match_version = regex.fullmatch(package["version"])

    #         if match_name or match_version:
    #             matched_packages.append(package)

    #     return matched_packages



    # def get_versions(self, repo, package_name):
    #     """Get versions of a given package on a specific repo"""

    #     cmd = f'/api/v1/repos/avidbots/{repo}/package/deb/ubuntu/xenial/{package_name}/amd64/versions.json'
    #     return self.get_objects(cmd)



    # def get_all_packages(self, repo):
    #     """Get all packages from a given repo"""

    #     cmd = f'/api/v1/repos/avidbots/{repo}/packages.json'
    #     return self.get_objects(cmd)







    # def delete_packages(self, packages):
    #     """Delete packages from packagecloud
        
    #     Args:
    #         packages: list of packages. Each item is a JSON object containing
    #                   the following elements:
    #         {
    #             "filename": "jakedotrb-0.0.1.gem",
    #             "destroy_url": "/api/v1/repos/test_user/test_repo/gems/jakedotrb-0.0.1.gem"
    #         }
                        
    #     """

    #     for package in packages:
    #         cmd = package['destroy_url']
    #         name = package['filename']

    #         request = delete_request(cmd)

    #         if request.status_code != 200:
    #             print(f'ERROR: HTTP return code: {request.status_code} ({cmd})')
    #         else:
    #             print(f'Successfully deleted {name}!')


    # def print_packages(self, packages):
    #     for package in packages:
    #         name = package['name'] 
    #         version = package['version']
    #         release = package['release']
    #         print(f'{name}_{version}-{release}')


    # def list_versions(self, repo, package_name):
    #     self.print_packages(self.get_versions(repo, package_name))


    # def list_packages(self, repo):
    #     self.print_packages(self.get_all_packages(repo))


    # def get_total_packages(self, repo):
    #     """Make GET request to packagecloud API
    #     """

    #     cmd = f'/api/v1/repos/avidbots/{repo}/packages.json'
    #     url = f'{self.url}/{cmd}?per_page=0'
        
    #     response = requests.get(url, timeout=120)
        
    #     if response.ok:
    #         return int(response.headers['Total'])
    #     else:
    #         return 0


if __name__ == '__main__':
    pass
