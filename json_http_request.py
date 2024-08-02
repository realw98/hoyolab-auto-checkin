import requests
from json import loads
import logging
from requests.exceptions import HTTPError

def json_http_request(method, url, headers, max_retry: int = 3, data=None, **kwargs):
    for i in range(max_retry + 1):
        try:
            s = requests.Session()
            response = s.request(method, url, data=data, headers=headers, **kwargs)
        except HTTPError as e:
            logging.error(f'HTTP error:\n{e}')
            logging.error(f'Request #{i + 1} failed, retrying...')
        except KeyError as e:
            logging.error(f'Wrong response:\n{e}')
            logging.error(f'Request #{i + 1} failed, retrying...')
        except Exception as e:
            logging.error(f'Unknown error:\n{e}')
            logging.error(f'Request #{i + 1} failed, retrying...')
        else:
            return loads(response.text)

    raise Exception(f'All {max_retry + 1} HTTP requests of {url} failed.')

