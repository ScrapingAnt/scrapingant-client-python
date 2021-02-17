import base64


def base64_encode_string(input_string: str) -> str:
    input_bytes = input_string.encode()
    base64_bytes = base64.b64encode(input_bytes)
    base64_string = base64_bytes.decode()
    return base64_string
