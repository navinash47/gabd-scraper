# Create initial channels
from django.utils import timezone

from scrapper.details import get_channels_details

initial_channel_ids = [
    "UCSHZKyawb77ixDdsGog4iWA",  # Lex Fridman
    "UCHnyfMqiRRG1u-2MsSQLbXA",  # Veritasium
]

print(f"{timezone.now()} Creating initial channels")
get_channels_details(initial_channel_ids)

# BlackList
from scrapper.models import BlackList

blacklist_domains = [
    "youtube.com",
    "youtu.be",
    "facebook.com",
    "instagram.com",
    "twitter.com",
    "tiktok.com",
    "patreon.com",
    "soundcloud.com",
    "linktr.ee",
    "spotify.com",
    "lexfridman.com",
    "hubermanlab.com",
]

for domain in blacklist_domains:
    print(f"Creating BlackList domain {domain}")
    BlackList.objects.get_or_create(domain=domain)
