from typing import List


class Cookie:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __eq__(self, other: 'Cookie'):
        return self.name == other.name and self.value == other.value

    def to_string(self) -> str:
        return f'{self.name}={self.value}'

    @classmethod
    def from_string(cls, cookie_string: str) -> 'Cookie':
        name, value = cookie_string.split('=', maxsplit=1)
        return cls(
            name=name,
            value=value,
        )


def cookies_list_to_string(cookies_list: List[Cookie]) -> str:
    return ';'.join([cookie.to_string() for cookie in cookies_list])


def cookies_list_from_string(cookies_string: str) -> List[Cookie]:
    return [
        Cookie.from_string(single_cookie_string)
        for single_cookie_string in cookies_string.split(';')
        if single_cookie_string
    ]
