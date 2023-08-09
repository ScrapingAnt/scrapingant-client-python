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
        responses.GET,
        url=SCRAPINGANT_API_BASE_URL +
        '/extended'
        '?url=http%3A%2F%2Fexample.com'
        '&cookies=test_name%3Dtest_value'
        '&js_snippet=dGVzdF9qc19zdHJpbmc%3D'
        '&proxy_type=datacenter'
        '&proxy_country=test_country'
        '&wait_for_selector=test_selector'
        '&browser=True'
        '&return_page_source=True',
        json={
            "html": "test_content",
            "cookies": "test_key1=test_value1;test_key2=test_value2",
            "text": "test_text",
            "status_code": 200,
        },
        status=200,
    )
    response = client.general_request(
        url='http://example.com',
        cookies=[Cookie('test_name', 'test_value')],
        headers={
            'testheader': 'test_header_value'},
        js_snippet='test_js_string',
        proxy_type=ProxyType.datacenter,
        proxy_country='test_country',
        wait_for_selector='test_selector',
        browser=True,
        return_page_source=True,
    )
    expected = {
        'content': 'test_content',
        'cookies': [Cookie('test_key1', 'test_value1'), Cookie('test_key2', 'test_value2')],
        "text": "test_text",
        'status_code': 200,
    }
    assert response.__dict__ == expected
    assert len(responses.calls) == 1

    headers = responses.calls[0].request.headers
    assert headers['ant-testheader'] == 'test_header_value'
    assert headers['x-api-key'] == 'test_token'


@pytest.mark.asyncio
async def test_integration_async(httpx_mock: HTTPXMock):
    client = ScrapingAntClient(token='test_token')
    httpx_mock.add_response(
        method="GET",
        url=SCRAPINGANT_API_BASE_URL +
        '/extended'
        '?url=http%3A%2F%2Fexample.com'
        '&cookies=test_name%3Dtest_value'
        '&js_snippet=dGVzdF9qc19zdHJpbmc%3D'
        '&proxy_type=datacenter'
        '&proxy_country=test_country'
        '&wait_for_selector=test_selector'
        '&browser=true'
        '&return_page_source=true',
        json={
            "html": "test_content",
            "cookies": "test_key1=test_value1;test_key2=test_value2",
            "text": "test_text",
            "status_code": 200,
        },
        status_code=200,
    )
    response = await client.general_request_async(
        url='http://example.com',
        cookies=[Cookie('test_name', 'test_value')],
        headers={
            'testheader': 'test_header_value'},
        js_snippet='test_js_string',
        proxy_type=ProxyType.datacenter,
        proxy_country='test_country',
        wait_for_selector='test_selector',
        browser=True,
        return_page_source=True,
    )
    expected = {
        'content': 'test_content',
        'cookies': [Cookie('test_key1', 'test_value1'), Cookie('test_key2', 'test_value2')],
        "text": "test_text",
        'status_code': 200,
    }
    assert response.__dict__ == expected
    assert len(httpx_mock.get_requests()) == 1

    headers = httpx_mock.get_requests()[0].headers
    assert headers['ant-testheader'] == 'test_header_value'
    assert headers['x-api-key'] == 'test_token'


@responses.activate
def test_post():
    client = ScrapingAntClient(token='test_token')
    responses.add(
        responses.POST,
        url=SCRAPINGANT_API_BASE_URL + '/extended',
        json={
            "html": "test_content",
            "cookies": "",
            "text": "test_text",
            "status_code": 200,
        },
        status=200,
    )
    client.general_request(
        url='http://example.com',
        method='POST',
        json={
            'test_key': 'test_value'},
    )

    assert len(responses.calls) == 1
    assert responses.calls[0].request.method == 'POST'
    assert json.loads(responses.calls[0].request.body) == {
        'test_key': 'test_value'}
    assert responses.calls[0].request.params == {
        'browser': 'True',
        'proxy_type': 'datacenter',
        'url': 'http://example.com',
    }

    headers = responses.calls[0].request.headers
    assert headers['x-api-key'] == 'test_token'
