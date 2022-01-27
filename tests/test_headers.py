from scrapingant_client.headers import convert_headers


def test_convert_empty_headers():
    assert convert_headers(None) is None


def test_convert_headers():
    headers = {
        'User-Agent': 'test',
        'Accept-Language': 'en-US'
    }
    assert convert_headers(headers) == {
        'ant-User-Agent': 'test',
        'ant-Accept-Language': 'en-US'
    }
