import platform
import sys
from typing import List, Optional

import requests

from scrapingant_client.constants import ProxyCountry
from scrapingant_client.cookie import Cookie, cookies_list_to_string, cookies_list_from_string
from scrapingant_client.response import Response
from scrapingant_client.utils import base64_encode_string


class ScrapingAntClient:
    def __init__(self, token: str):
        self.token = token
        self.scrapingant_api_base_url = 'https://api.scrapingant.com/v1'
        self.requests_session = requests.Session()
        user_agent = f'ScrapingAntClient ({sys.platform}; Python/{platform.python_version()});'
        self.requests_session.headers.update({
            'x-api-key': self.token,
            'User-Agent': user_agent,
        })

    def general_request(
            self,
            url: str,
            cookies: Optional[List[Cookie]] = None,
            js_snippet: Optional[str] = None,
            proxy_country: Optional[ProxyCountry] = None,
            return_text: bool = False,
    ) -> Response:
        request_data = {'url': url}
        if cookies is not None:
            request_data['cookies'] = cookies_list_to_string(cookies)
        if js_snippet is not None:
            encoded_js_snippet = base64_encode_string(js_snippet)
            request_data['js_snippet'] = encoded_js_snippet
        if proxy_country:
            request_data['proxy_country'] = proxy_country.lower()
        if return_text:
            request_data['return_text'] = True

        response = self.requests_session.post(
            self.scrapingant_api_base_url + '/general',
            json=request_data,
        )
        json_response = response.json()
        content = json_response['content']
        cookies_string = json_response['cookies']
        cookies_list = cookies_list_from_string(cookies_string)
        return Response(
            content=content,
            cookies=cookies_list,
        )
