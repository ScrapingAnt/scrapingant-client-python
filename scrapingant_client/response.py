from typing import List, Optional

from scrapingant_client.cookie import Cookie


class Response:
    def __init__(self, content: str, cookies: List[Cookie], text: str, status_code: Optional[int]):
        self.content = content
        self.cookies = cookies
        self.text = text
        self.status_code = status_code


class MarkdownResponse:
    def __init__(self, url: str, markdown: str):
        self.url = url
        self.markdown = markdown
