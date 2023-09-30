ignore_brand_domains = [
    "www.amazon.com",
    "www.amazon.in",
    "amazon.com",
    "amazon.in",
    "www.amazon.co.uk",
    "geni.us",
    "www.aliexpress.com",
]

# Ignore domains that contain these words
ignore_words = ["amazon"]


def filter_domains(domains):
    ig_bd = [domain for domain in domains if domain not in ignore_brand_domains]
    ig_wd = [
        domain for domain in ig_bd if not any(word in domain for word in ignore_words)
    ]
    return ig_wd


def accept_domain(domain):
    if not domain or domain in ignore_brand_domains:
        return False
    if any(word in domain for word in ignore_words):
        return False
    return True
