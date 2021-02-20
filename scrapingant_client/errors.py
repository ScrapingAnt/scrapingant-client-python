class ScrapingantClientException(Exception):
    """Base class for errors specific to the ScrapingAnt Client."""
    pass


class ScrapingantInvalidTokenException(ScrapingantClientException):
    def __init__(self):
        message = 'API token is wrong or you have exceeded the API calls request limit'
        super().__init__(message)


class ScrapingantInvalidInputException(ScrapingantClientException):
    pass


class ScrapingantInternalException(ScrapingantClientException):
    def __init__(self):
        message = 'Something went wrong with the server side. Please try later or contact support'
        super().__init__(message)
