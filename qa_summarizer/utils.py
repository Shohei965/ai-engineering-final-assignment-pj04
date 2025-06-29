import re


def extract_sheet_id(url: str) -> str:
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if not match:
        raise ValueError('Invalid Google Sheet URL')
    return match.group(1)
