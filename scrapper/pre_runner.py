# Create initial channels
from django.utils import timezone

from scrapper.details import get_channels_details

initial_channel_ids = [
    "UCSHZKyawb77ixDdsGog4iWA",  # Lex Fridman
    "UCHnyfMqiRRG1u-2MsSQLbXA",  # Veritasium
    "UCP5tjEmvPItGyLhmjdwP7Ww",  # RealLifeLore
    "UCbiGcwDWZjz05njNPrJU7jA",  # ExplainingComputers
    "UC-2YHgc363EdcusLIBbgxzg",  # Joe Scott
    "UC0intLFzLaudFG-xAvUEO-A",  # Not Just Bikes
    "UCfdNM3NAhaBOXCafH7krzrA",  # The Infographics Show
    "UCMiJRAwDNSNzuYeN2uWa0pA",  # Mrwhosetheboss
    "UCR-DXc1voovS8nhAvccRZhg",  # Jeff Geerling
    "UCRcgy6GzDeccI7dkbbBna3Q",  # LEMMiNO
    "UC8kGsMa0LygSX9nkBcBH1Sg",  # Peter Attia MD
    "UCH4BNI0-FOK2dMXoFtViWHw",  # Be Smart
    "UC9RM-iSvTu1uPJb8X5yp3EQ",  # Wendover Productions
    "UC2D2CMWXMOVWx7giW1n3LIg",  # Andrew Huberman
    "UCmGSJVG3mCRXVOP4yZrU1Dw",  # Johnny Harris
    "UC6107grRI4m0o2-emgoDnAA",  # SmarterEveryDay
    "UCR1IuLEqb6UEA_zQ81kwXfg",  # Real Engineering
    "UCbk_QsfaFZG6PdQeCvaYXJQ",  # Jay Shetty Podcast
    "UCIaH-gZIVC432YRjNVvnyCA",  # Chris Williamson
    "UCUeZBocfxALSUdOgNJB5ySA",  # Dr Ben Miles
    "UCFtc3XdXgLFwhlDajMGK69w",  # NightHawkInLight
    "UCMOqf8ab-42UUQIdVoKwjlQ",  # Practical Engineering
    "UCPxMZIFE856tbTfdkdjzTSQ",  # BeerBiceps
    "UCEIwxahdLz7bap-VDs9h35A",  # Steve Mould
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
    print(f"{timezone.now()} Creating BlackList domain {domain}")
    BlackList.objects.get_or_create(domain=domain)
