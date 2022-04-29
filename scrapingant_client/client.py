import platform
import sys
from typing import List, Optional, Dict

import requests

import scrapingant_client
from scrapingant_client.constants import SCRAPINGANT_API_BASE_URL
from scrapingant_client.cookie import Cookie, cookies_list_to_string, cookies_list_from_string
from scrapingant_client.errors import (
    ScrapingantInvalidTokenException,
    ScrapingantInvalidInputException,
    ScrapingantInternalException,
    ScrapingantSiteNotReachableException,
    ScrapingantDetectedException,
)
from scrapingant_client.headers import convert_headers
from scrapingant_client.proxy_type import ProxyType
from scrapingant_client.response import Response
from scrapingant_client.utils import base64_encode_string


class ScrapingAntClient:
    def __init__(self, token: str):
        self.token = token
        self.requests_session = requests.Session()
        version = scrapingant_client.__version__
        user_agent = f'ScrapingAnt Client/{version} ({sys.platform}; Python/{platform.python_version()});'
        self.requests_session.headers.update({
            'x-api-key': self.token,
            'User-Agent': user_agent,
        })

    def general_request(
            self,
            url: str,
            cookies: Optional[List[Cookie]] = None,
            headers: Optional[Dict[str, str]] = None,
            js_snippet: Optional[str] = None,
            proxy_type: ProxyType = ProxyType.datacenter,
            proxy_country: Optional[str] = None,
            return_text: bool = False,
            wait_for_selector: Optional[str] = None,
            browser: bool = True,
    ) -> Response:
        request_data = {'url': url}
        if cookies is not None:
            request_data['cookies'] = cookies_list_to_string(cookies)
        if js_snippet is not None:
            encoded_js_snippet = base64_encode_string(js_snippet)
            request_data['js_snippet'] = encoded_js_snippet
        request_data['proxy_type'] = proxy_type
        if proxy_country is not None:
            request_data['proxy_country'] = proxy_country.lower()
        if wait_for_selector is not None:
            request_data['wait_for_selector'] = wait_for_selector
        request_data['return_text'] = return_text
        request_data['browser'] = browser

        response = self.requests_session.post(
            SCRAPINGANT_API_BASE_URL + '/general',
            json=request_data,
            headers=convert_headers(headers),
        )
        if response.status_code == 403:
            raise ScrapingantInvalidTokenException()
        elif response.status_code == 404:
            raise ScrapingantSiteNotReachableException(url)
        elif response.status_code == 422:
            raise ScrapingantInvalidInputException(response.text)
        elif response.status_code == 423:
            raise ScrapingantDetectedException()
        elif response.status_code == 500:
            raise ScrapingantInternalException()
        json_response = response.json()
        content = json_response['content']
        cookies_string = json_response['cookies']
        status_code = json_response['status_code']
        cookies_list = cookies_list_from_string(cookies_string)
        return Response(
            content=content,
            cookies=cookies_list,
            status_code=status_code
        )
