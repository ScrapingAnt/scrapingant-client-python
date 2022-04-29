from typing import List, Optional

from scrapingant_client.cookie import Cookie


class Response:
    def __init__(self, content: str, cookies: List[Cookie], status_code: Optional[int]):
        self.content = content
        self.cookies = cookies
        self.status_code = status_code
