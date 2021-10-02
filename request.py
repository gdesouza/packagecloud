import logging
import requests


class Request:
    """
    A class used to send API requests.
    """
    
    def __init__(self, url, timeout=120):
        """
        Parameters
        ----------
        url : str
        timeout : int, optional
        """

        self.url = url
        self.timeout = timeout
        self._params = None
    
    @property
    def params(self):
        """
        Returns
        -------
        The request parameters for the URL
        """

        return self._params

    @params.setter
    def params(self, params):
        """Sets the URL parameters
        Parameters
        ----------
        params : dict
            Dictionary with URL parameters
        """

        self._params = params

    def _get_request(self, path, page=1):
        """Internal get_request method

        Parameters
        ----------
        path : str
            The URL path
        page : int,optional

        Returns
        -------
        The request response
        """

        url = f'{self.url}/{path}?page={page}'
        if self.params:
            url += f'&{self.params}'

        logging.debug(f'Request: {url}')
        return requests.get(url, timeout=self.timeout)
        
    def get(self, path, params=None):
        """ Make GET request to API

        Parameters
        ========== 
        path: str
            API resource path
        params: dict,optional
            Key value pair of parameters
        """

        page = 1
        objects = []

        self.params = params

        response = self._get_request(path)
        logging.debug(response.text)

        # if not 200 OK
        if not response.ok:
            logging.error(f'ERROR: HTTP return code: {response.status_code} ({path})')
            return objects

        # always use the total number of packages returned by first 
        # request as the reference
        objects.append(response.json())

        total = int(response.headers.get("Total", 0))
        read = len(objects)

        logging.debug(f'Reading {read} of {total}')

        while read < total:
            page += 1
            response = self._get_request(path, page)

            # if not 200 OK
            if not response.ok:
                logging.error(f"Download interrupted due to request error: {response.status_code}")
                break

            objects += response.json()
            read = len(objects)

            logging.debug(f'Reading {read} of {total}')

        # sanity check, since multiple requests are made. We might have race
        # conditions. Inform user if there are anything strange going on
        if len(objects) != total:
            logging.warning('Number of retrieved objects does not match ' +
                   f'({len(objects)} retrieved, should be {total})' )

        return objects


if __name__ == '__main__':
    pass
