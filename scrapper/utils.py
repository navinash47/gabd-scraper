import re


def get_domain(url):
    """
    Get the domain name from a URL.
    """
    pattern = r"(?:https?://)?([^/]+)"
    match = re.search(pattern, url)
    if match:
        domain = match.group(1)
        # Remove 'www.' if it's in the domain
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    return None


def print_exception(e):
    with open("error.txt", "a") as f:
        f.write(str(e) + "\n")
