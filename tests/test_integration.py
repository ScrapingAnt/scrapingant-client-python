import json

import pytest
import responses
from pytest_httpx import HTTPXMock

from scrapingant_client import ScrapingAntClient, Cookie, ProxyType
from scrapingant_client.constants import SCRAPINGANT_API_BASE_URL


@responses.activate
def test_integration():
    client = ScrapingAntClient(token='test_token')
    responses.add(
        responses.POST,
        url=SCRAPINGANT_API_BASE_URL + '/general',
        json={
            "content": "test_content",
            "cookies": "test_key1=test_value1;test_key2=test_value2",
            "status_code": 200,
        },
        status=200,
    )
    response = client.general_request(
        url='http://example.com',
        cookies=[Cookie('test_name', 'test_value')],
        headers={'testheader': 'test_header_value'},
        js_snippet='test_js_string',
        proxy_type=ProxyType.datacenter,
        proxy_country='test_country',
        return_text=True,
        wait_for_selector='test_selector',
        browser=True,
    )
    expected = {
        'content': 'test_content',
        'cookies': [Cookie('test_key1', 'test_value1'), Cookie('test_key2', 'test_value2')],
        'status_code': 200
    }
    assert response.__dict__ == expected
    assert len(responses.calls) == 1

    expected_body = {
        'browser': True,
        'cookies': 'test_name=test_value',
        'js_snippet': 'dGVzdF9qc19zdHJpbmc=',
        'proxy_country': 'test_country',
        'proxy_type': 'datacenter',
        'return_text': True,
        'url': 'http://example.com',
        'wait_for_selector': 'test_selector',
    }
    assert json.loads(responses.calls[0].request.body) == expected_body

    headers = responses.calls[0].request.headers
    assert headers['ant-testheader'] == 'test_header_value'
    assert headers['x-api-key'] == 'test_token'


@pytest.mark.asyncio
async def test_integration_async(httpx_mock: HTTPXMock):
    client = ScrapingAntClient(token='test_token')
    httpx_mock.add_response(
        method="POST",
        url=SCRAPINGANT_API_BASE_URL + '/general',
        json={
            "content": "test_content",
            "cookies": "test_key1=test_value1;test_key2=test_value2",
            "status_code": 200,
        },
        status_code=200,
    )
    response = await client.general_request_async(
        url='http://example.com',
        cookies=[Cookie('test_name', 'test_value')],
        headers={'testheader': 'test_header_value'},
        js_snippet='test_js_string',
        proxy_type=ProxyType.datacenter,
        proxy_country='test_country',
        return_text=True,
        wait_for_selector='test_selector',
        browser=True,
    )
    expected = {
        'content': 'test_content',
        'cookies': [Cookie('test_key1', 'test_value1'), Cookie('test_key2', 'test_value2')],
        'status_code': 200
    }
    assert response.__dict__ == expected
    assert len(httpx_mock.get_requests()) == 1

    expected_body = {
        'browser': True,
        'cookies': 'test_name=test_value',
        'js_snippet': 'dGVzdF9qc19zdHJpbmc=',
        'proxy_country': 'test_country',
        'proxy_type': 'datacenter',
        'return_text': True,
        'url': 'http://example.com',
        'wait_for_selector': 'test_selector',
    }
    assert json.loads(httpx_mock.get_requests()[0].content) == expected_body

    headers = httpx_mock.get_requests()[0].headers
    assert headers['ant-testheader'] == 'test_header_value'
    assert headers['x-api-key'] == 'test_token'
