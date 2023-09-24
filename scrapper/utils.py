import re


def get_domain(url):
    """
    Get the domain name from a URL.
    """
    domain_regex = r"(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n]+)"
    return re.search(domain_regex, url).group(1)


def print_exception(e):
    with open("error.txt", "a") as f:
        f.write(str(e) + "\n")
