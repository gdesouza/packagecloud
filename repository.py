import logging
from packagecloud import BasePackageCloudClient
from request import Request


class RepositoryClient(BasePackageCloudClient):
    """Repository settings class"""

    def __init__(self, user, repo, distro, api_token):
        """
        Parameters
        ----------
        user : str
        repo : str
        distro : str
        api_token : str
        """
        super().__init__(api_token)
        self.user = user
        self.repo = repo
        self.distro = distro

    @property
    def packages_path(self):
        return f'{self.repo_path}/packages.json'

    @property
    def repo_path(self):
        return f'repos/{self.user}/{self.repo}'

    def get_packages(self):
        """Get all packages from a given repo"""

        return Request(self.url_base).get(self.packages_path)

    def get_number_of_packages(self):
        """Get number of packages in the repo"""
        
        info = Request(self.url_base).get(self.packages_path)[0]
        logging.debug(f"Info request returned: {info}")
        return int(info.get('package_count_human', 0))
        
    # def get(self, path, parms, page=1):
    #     """Make GET request to packagecloud API
    #     """

    #     url = f'{self.url_base}/{path}?page={page}'
    #     if parms:
    #         url += f'&{self.dict_to_url_params(parms)}'

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
