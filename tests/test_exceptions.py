import pytest
import responses

from scrapingant_client import (
    ScrapingAntClient,
    ScrapingantInvalidTokenException,
    ScrapingantInvalidInputException,
    ScrapingantInternalException,
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
