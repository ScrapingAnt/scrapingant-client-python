from scrapingant_client import Cookie
from scrapingant_client.cookie import cookies_list_to_string, cookies_list_from_string


def test_cookies_list_to_string_empty():
    assert cookies_list_to_string([]) == ''


def test_cookies_list_to_string():
    cookies = [
        Cookie(
            name='test_name1',
            value='test_value1'
        ),
        Cookie(
            name='test_name2',
            value='test_value2'
        ),
    ]
    assert cookies_list_to_string(cookies) == 'test_name1=test_value1;test_name2=test_value2'


def test_cookies_list_from_string_empty():
    assert cookies_list_from_string('') == []


def test_cookies_list_from_string():
    actual = cookies_list_from_string('test_name1=test_value1;test_name2=test_value2')
    expected = [
        Cookie(
            name='test_name1',
            value='test_value1'
        ),
        Cookie(
            name='test_name2',
            value='test_value2'
        ),
    ]
    assert actual == expected
