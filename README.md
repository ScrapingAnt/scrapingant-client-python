# ScrapingAnt API client for Python

[![PyPI version](https://badge.fury.io/py/scrapingant-client.svg)](https://badge.fury.io/py/scrapingant-client)

`scrapingant-client` is the official library to access [ScrapingAnt API](https://docs.scrapingant.com) from your Python
applications. It provides useful features like parameters encoding to improve the ScrapingAnt usage experience. Requires
python 3.6+.

<!-- toc -->

- [Quick Start](#quick-start)
- [API token](#api-token)
- [API Reference](#api-reference)
- [Exceptions](#exceptions)
- [Examples](#examples)
- [Useful links](#useful-links)

<!-- tocstop -->

## Quick Start

```python3
from scrapingant_client import ScrapingAntClient

client = ScrapingAntClient(token='<YOUR-SCRAPINGANT-API-TOKEN>')
# Scrape the example.com site.
result = client.general_request('https://example.com')
print(result.content)
```

## Install

```shell
pip install scrapingant-client
```

If you need async support:

```shell
pip install scrapingant-client[async]
```

## API token

In order to get API token you'll need to register at [ScrapingAnt Service](https://app.scrapingant.com)

## API Reference

All public classes, methods and their parameters can be inspected in this API reference.

#### ScrapingAntClient(token)

Main class of this library.

| Param | Type  |
| --- | --- |
| token | <code>string</code> |

* * *

#### ScrapingAntClient.general_request and ScrapingAntClient.general_request_async

https://docs.scrapingant.com/request-response-format#available-parameters

| Param | Type | Default |
| --- | --- | --- |
| url | <code>string</code> |  |
| cookies | <code>List[Cookie]</code> | None |
| headers | <code>List[Dict[str, str]]</code> | None |
| js_snippet | <code>string</code> | None |
| proxy_type | <code>ProxyType</code> | datacenter | 
| proxy_country | <code>str</code> | None | 
| return_text | <code>boolean</code> | False |
| wait_for_selector | <code>str</code> | None |
| browser | <code>boolean</code> | True |

**IMPORTANT NOTE:** <code>js_snippet</code> will be encoded to Base64 automatically by the ScrapingAnt client library.

* * *

#### Cookie

Class defining cookie. Currently it supports only name and value

| Param | Type | 
| --- | --- |
| name | <code>string</code> | 
| value | <code>string</code> |

* * *

#### Response

Class defining response from API.

| Param | Type |
| --- | --- |
| content | <code>string</code> |
| cookies | <code>List[Cookie]</code> |
| status_code | <code>int</code> |

## Exceptions

`ScrapingantClientException` is base Exception class, used for all errors.

| Exception | Reason |
| --- | --- |
| ScrapingantInvalidTokenException | The API token is wrong or you have exceeded the API calls request limit
| ScrapingantInvalidInputException | Invalid value provided. Please, look into error message for more info |
| ScrapingantInternalException | Something went wrong with the server side code. Try again later or contact ScrapingAnt support |
| ScrapingantSiteNotReachableException | The requested URL is not reachable. Please, check it locally |
| ScrapingantDetectedException | The anti-bot detection system has detected the request. Please, retry or change the request settings. |

* * *

## Examples

### Sending custom cookies

```python3
from scrapingant_client import ScrapingAntClient
from scrapingant_client import Cookie

client = ScrapingAntClient(token='<YOUR-SCRAPINGANT-API-TOKEN>')

result = client.general_request(
    'https://httpbin.org/cookies',
    cookies=[
        Cookie(name='cookieName1', value='cookieVal1'),
        Cookie(name='cookieName2', value='cookieVal2'),
    ]
)
print(result.content)
# Response cookies is a list of Cookie objects
# They can be used in next requests
response_cookies = result.cookies 
```

### Executing custom JS snippet

```python
from scrapingant_client import ScrapingAntClient

client = ScrapingAntClient(token='<YOUR-SCRAPINGANT-API-TOKEN>')

customJsSnippet = """
var str = 'Hello, world!';
var htmlElement = document.getElementsByTagName('html')[0];
htmlElement.innerHTML = str;
"""
result = client.general_request(
    'https://example.com',
    js_snippet=customJsSnippet,
)
print(result.content)
```

### Exception handling and retries

```python
from scrapingant_client import ScrapingAntClient, ScrapingantClientException, ScrapingantInvalidInputException

client = ScrapingAntClient(token='<YOUR-SCRAPINGANT-API-TOKEN>')

RETRIES_COUNT = 3


def parse_html(html: str):
    ...  # Implement your data extraction here


parsed_data = None
for retry_number in range(RETRIES_COUNT):
    try:
        scrapingant_response = client.general_request(
            'https://example.com',
        )
    except ScrapingantInvalidInputException as e:
        print(f'Got invalid input exception: {{repr(e)}}')
        break  # We are not retrying if request params are not valid
    except ScrapingantClientException as e:
        print(f'Got ScrapingAnt exception {repr(e)}')
    except Exception as e:
        print(f'Got unexpected exception {repr(e)}')  # please report this kind of exceptions by creating a new issue
    else:
        try:
            parsed_data = parse_html(scrapingant_response.content)
            break  # Data is parsed successfully, so we dont need to retry
        except Exception as e:
            print(f'Got exception while parsing data {repr(e)}')

if parsed_data is None:
    print(f'Failed to retrieve and parse data after {RETRIES_COUNT} tries')
    # Can sleep and retry later, or stop the script execution, and research the reason 
else:
    print(f'Successfully parsed data: {parsed_data}')
```

### Sending custom headers

```python3
from scrapingant_client import ScrapingAntClient

client = ScrapingAntClient(token='<YOUR-SCRAPINGANT-API-TOKEN>')

result = client.general_request(
    'https://httpbin.org/headers',
    headers={
        'test-header': 'test-value'
    }
)
print(result.content)

# Http basic auth example
result = client.general_request(
    'https://jigsaw.w3.org/HTTP/Basic/',
    headers={'Authorization': 'Basic Z3Vlc3Q6Z3Vlc3Q='}
)
print(result.content)
```

### Simple async example

```python3
import asyncio

from scrapingant_client import ScrapingAntClient

client = ScrapingAntClient(token='<YOUR-SCRAPINGANT-API-TOKEN>')


async def main():
    # Scrape the example.com site.
    result = await client.general_request_async('https://example.com')
    print(result.content)


asyncio.run(main())
```

## Useful links

- [Scrapingant API doumentation](https://docs.scrapingant.com)
- [Scrapingant JS Client](https://github.com/scrapingant/scrapingant-client-js)
