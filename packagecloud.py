import logging


class BasePackageCloudClient:
    """Interface class to use packagecloud.io API"""

    def __init__(self,
                 api_token,
                 http_scheme='https', 
                 api_domain='packagecloud.io', 
                 api_version='v1'):
        """
        Parameters
        ----------
        api_token : string
        http_scheme : string,optional
        api_domain : string,optional
        api_version : str,optional
        """
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
