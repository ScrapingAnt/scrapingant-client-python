from typing import Dict, Optional


def convert_headers(headers: Optional[Dict[str, str]]):
    if headers is None:
        return None
    return {
        f'ant-{header_name}': header_value
        for header_name, header_value in headers.items()
    }
