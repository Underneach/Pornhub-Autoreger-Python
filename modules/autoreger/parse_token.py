import re


def Parse_Token(html_body):

    pattern = r'token\s*=\s*"([^"]+)"'
    match = re.search(pattern, html_body)
    token_value = match.group(1)

    return token_value
