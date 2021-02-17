from typing import List

from src.cookie import Cookie


class Response:
    def __init__(self, content: str, cookies: List[Cookie]):
        self.content = content
        self.cookies = cookies
