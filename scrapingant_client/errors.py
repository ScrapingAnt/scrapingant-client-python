class ScrapingantClientException(Exception):
    """Base class for errors specific to the ScrapingAnt Client."""
    pass


class ScrapingantInvalidTokenException(ScrapingantClientException):
    def __init__(self):
        message = 'API token is wrong or you have exceeded the API calls request limit'
        super().__init__(message)


class ScrapingantInvalidInputException(ScrapingantClientException):
    pass


class ScrapingantSiteNotReachableException(ScrapingantClientException):
    def __init__(self, url):
        message = f'The requested URL is not reachable ({url})'
        super().__init__(message)


class ScrapingantDetectedException(ScrapingantClientException):
    def __init__(self):
        message = 'The anti-bot detection system has detected the request. ' \
                  'Please, retry or change the request settings.'
        super().__init__(message)


class ScrapingantInternalException(ScrapingantClientException):
    def __init__(self):
        message = 'Something went wrong with the server side. Please try later or contact support'
        super().__init__(message)


class ScrapingantTimeoutException(ScrapingantClientException):
    def __init__(self):
        message = 'Got timeout while communicating with Scrapingant servers.' \
                  ' Check your network connection. Please try later or contact support'
        super().__init__(message)
