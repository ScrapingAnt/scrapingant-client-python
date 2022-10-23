import platform
import sys
from typing import List, Optional, Dict

import requests

import scrapingant_client
from scrapingant_client.constants import SCRAPINGANT_API_BASE_URL, TIMEOUT_SECONDS
from scrapingant_client.cookie import Cookie, cookies_list_to_string, cookies_list_from_string
from scrapingant_client.errors import (
    ScrapingantInvalidTokenException,
    ScrapingantInvalidInputException,
    ScrapingantInternalException,
    ScrapingantSiteNotReachableException,
    ScrapingantDetectedException,
    ScrapingantTimeoutException,
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
        self.user_agent = f'ScrapingAnt Client/{version} ({sys.platform}; Python/{platform.python_version()});'
        self.requests_session.headers.update({
            'x-api-key': self.token,
            'User-Agent': self.user_agent,
        })

    def _form_payload(
            self,
            url: str,
            cookies: Optional[List[Cookie]] = None,
            js_snippet: Optional[str] = None,
            proxy_type: ProxyType = ProxyType.datacenter,
            proxy_country: Optional[str] = None,
            return_text: bool = False,
            wait_for_selector: Optional[str] = None,
            browser: bool = True,
    ) -> Dict:
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
        return request_data

    def _parse_response(self, response_status_code: int, response_data: Dict, url: str) -> Response:
        if response_status_code == 403:
            raise ScrapingantInvalidTokenException()
        elif response_status_code == 404:
            raise ScrapingantSiteNotReachableException(url)
        elif response_status_code == 422:
            raise ScrapingantInvalidInputException(response_data)
        elif response_status_code == 423:
            raise ScrapingantDetectedException()
        elif response_status_code == 500:
            raise ScrapingantInternalException()
        content = response_data['content']
        cookies_string = response_data['cookies']
        status_code = response_data['status_code']
        cookies_list = cookies_list_from_string(cookies_string)
        return Response(
            content=content,
            cookies=cookies_list,
            status_code=status_code
        )

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
        request_data = self._form_payload(
            url=url,
            cookies=cookies,
            js_snippet=js_snippet,
            proxy_type=proxy_type,
            proxy_country=proxy_country,
            return_text=return_text,
            wait_for_selector=wait_for_selector,
            browser=browser,
        )
        try:
            response = self.requests_session.post(
                SCRAPINGANT_API_BASE_URL + '/general',
                json=request_data,
                headers=convert_headers(headers),
                timeout=TIMEOUT_SECONDS
            )
        except requests.exceptions.Timeout:
            raise ScrapingantTimeoutException()
        response_status_code = response.status_code
        response_data = response.json()
        parsed_response: Response = self._parse_response(response_status_code, response_data, url)
        return parsed_response

    async def general_request_async(
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
        import httpx

        request_data = self._form_payload(
            url=url,
            cookies=cookies,
            js_snippet=js_snippet,
            proxy_type=proxy_type,
            proxy_country=proxy_country,
            return_text=return_text,
            wait_for_selector=wait_for_selector,
            browser=browser,
        )
        async with httpx.AsyncClient(
                headers={
                    'x-api-key': self.token,
                    'User-Agent': self.user_agent,
                },
                timeout=TIMEOUT_SECONDS,
        ) as client:
            try:
                response = await client.post(
                    SCRAPINGANT_API_BASE_URL + '/general',
                    json=request_data,
                    headers=convert_headers(headers),
                )
            except httpx.TimeoutException:
                raise ScrapingantTimeoutException()

        response_status_code = response.status_code
        response_data = response.json()
        parsed_response: Response = self._parse_response(response_status_code, response_data, url)
        return parsed_response
