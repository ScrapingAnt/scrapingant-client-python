# ScrapingAnt API client for Python
[![PyPI version](https://badge.fury.io/py/scrapingant-client.svg)](https://badge.fury.io/py/scrapingant-client)

`scrapingant-client` is the official library to access [ScrapingAnt API](https://docs.scrapingant.com) from your
Python applications. It  provides useful features like parameters encoding to improve the ScrapingAnt usage experience. 
Requires python 3.6+.

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

#### ScrapingAntClient.general_request

https://docs.scrapingant.com/request-response-format#available-parameters

| Param | Type | Default |
| --- | --- | --- |
| url | <code>string</code> |  |
| cookies | <code>List[Cookie]</code> | None |
| js_snippet | <code>string</code> | None |
| proxy_country | <code>str</code> | None | 
| return_text | <code>boolean</code> | False |

**IMPORTANT NOTE:** <code>js_snippet</code> will be encoded to Base64 automatically by the ScrapingAnt client library.

* * *

#### Cookie
Class defining cookie. Curently supports only name and value

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

## Exceptions

`ScrapingantClientException` is base Exception class, used for all errors. 

| Exception | Reason |
| --- | --- |
| ScrapingantInvalidTokenException | The API token is wrong or you have exceeded the API calls request limit 
| ScrapingantInvalidInputException | Invalid value provided. Please, look into error message for more info |
| ScrapingantInternalException | Something went wrong with the server side code. Try again later or contact ScrapingAnt support |
| ScrapingantSiteNotReachableException | The requested URL is not reachable. Please, check it locally |

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

## Useful links
- [Scrapingant API doumentation](https://docs.scrapingant.com)
- [Scrapingant JS Client](https://github.com/scrapingant/scrapingant-client-js)
