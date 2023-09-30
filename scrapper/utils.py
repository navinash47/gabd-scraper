import re


def get_domain(url):
    """
    Get the domain name from a URL.
    """
    pattern = r"(?:https?://)?([^/]+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


def print_exception(e):
    with open("error.txt", "a") as f:
        f.write(str(e) + "\n")
