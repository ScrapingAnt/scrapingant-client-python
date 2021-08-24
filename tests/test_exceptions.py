import pytest
import responses

from scrapingant_client import (
    ScrapingAntClient,
    ScrapingantInvalidTokenException,
    ScrapingantInvalidInputException,
    ScrapingantInternalException,
    ScrapingantSiteNotReachableException,
    ScrapingantDetectedException,
)
from scrapingant_client.constants import SCRAPINGANT_API_BASE_URL


@responses.activate
def test_invalid_token():
    responses.add(responses.POST, SCRAPINGANT_API_BASE_URL + '/general',
                  json={'detail': 'wrong token'}, status=403)
    client = ScrapingAntClient(token='invalid_token')
    with pytest.raises(ScrapingantInvalidTokenException):
        client.general_request('example.com')


@responses.activate
def test_invalid_input():
    responses.add(responses.POST, SCRAPINGANT_API_BASE_URL + '/general',
                  json={'detail': 'wrong url'}, status=422)
    client = ScrapingAntClient(token='some_token')
    with pytest.raises(ScrapingantInvalidInputException) as e:
        client.general_request('bad_url')
    assert '{"detail": "wrong url"}' in str(e)


@responses.activate
def test_internal_server_error():
    responses.add(responses.POST, SCRAPINGANT_API_BASE_URL + '/general',
                  json={}, status=500)
    client = ScrapingAntClient(token='some_token')
    with pytest.raises(ScrapingantInternalException):
        client.general_request('bad_url')


@responses.activate
def test_not_reachable():
    responses.add(responses.POST, SCRAPINGANT_API_BASE_URL + '/general',
                  json={}, status=404)
    client = ScrapingAntClient(token='some_token')
    with pytest.raises(ScrapingantSiteNotReachableException) as e:
        client.general_request('example.com')
    assert 'The requested URL is not reachable (example.com)' in str(e)


@responses.activate
def test_detected():
    responses.add(responses.POST, SCRAPINGANT_API_BASE_URL + '/general',
                  json={}, status=423)
    client = ScrapingAntClient(token='some_token')
    with pytest.raises(ScrapingantDetectedException) as e:
        client.general_request('example.com')
    assert 'The anti-bot detection system has detected the request' in str(e)
