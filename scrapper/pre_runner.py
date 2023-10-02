# Create initial channels
from django.utils import timezone

from scrapper.details import get_channels_details

initial_channel_ids = [
    # Round 1
    "UCSHZKyawb77ixDdsGog4iWA",  # Lex Fridman
    "UCsBjURrPoezykLs9EqgamOA",  # Fireship
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
    # Round 2
    "UC5H_lY2y5X3zhjy5KTez-vQ",  # Anita Bokepalli
    "UCkkhmBWfS7pILYIk0izkc3A",  # This Week in Startups
    "UC5AQEUAwCh1sGDvkQtkDWUQ",  # Theo Von
    # Round 3
    "UC3ETCazlHenpXEsrEJH-k5A",  # The Anime Man
    "UChBEbMKI1eCcejTtmI32UEw",  # Joshua Weissman
    "UCX6OQ3DkcsbYNE6H8uQQuVA",  # MrBeast
    "UCMyOj6fhvKFMjxUCp3b_3gA",  # Nick DiGiovanni
    "UCjPYYvIdTqn9U52p9IxJ72Q",  # Isaiah Photo
    "UCnmGIkw-KdI0W5siakKPKog",  # Ryan Trahan
    "UCyps-v4WNjWDnYRKmZ4BUGw",  # Airrack
    "UC7dF9qfBMXrSlaaFFDvV_Yg",  # Gigguk
    "UCDq5v10l4wkV5-ZBIJJFbzQ",  # Ethan Chlebowski
    "UCOq-wLPeAhS9TgMEClxwuOg",  # Sage's Rain
    "UCHL9bfHTxCMi-7vfxQ-AYtg",  # Abroad in Japan
    "UCv0jmyEcRipJqGV2i-P2jhA",  # SHUNchan
    "UCAzKFALPuF_EPe-AEI0WFFw",  # TwoSetViolin
    "UC_ozVYyGkVQBaaXI9jrCFqQ",  # Keo Tsang
    "UCnrVURWNd7VYjlQQ0UDpOQQ",  # Tokyo Lens
    "UCqwxJts-6yF33rupyF_DCsA",  # Life Where I'm From
    "UCzH5n3Ih5kgQoiDAQt2FwLw",  # Pro Home Cooks
    "UCJHA_jMfCvEnv-3kRjTCQXw",  # Babish Culinary Universe
    "UCrroaGjAjAjqXEjqdsjLMIw",  # Currently Hannah
]

print(f"{timezone.now()} Creating initial channels")
get_channels_details(initial_channel_ids)

# BlackList
from scrapper.models import BlackList, Brand

blacklist_domains = [
    "www.youtube.com",
    "youtube.com",
    "youtu.be",
    "facebook.com",
    "www.facebook.com",
    "instagram.com",
    "www.instagram.com",
    "twitter.com",
    "www.twitter.com",
    "tiktok.com",
    "www.tiktok.com",
    "patreon.com",
    "www.patreon.com",
    "soundcloud.com",
    "www.soundcloud.com",
    "linktr.ee",
    "www.linktr.ee",
    "spotify.com",
    "www.spotify.com",
    "lexfridman.com",
    "fireship.io",
    "hubermanlab.com",
    "peterattiamd.com",
    "linkedin.com",
    "www.linkedin.com",
    "paypal.com",
    "www.paypal.com",
    "threads.net",
    "www.threads.net",
    "music.apple.com",
    "open.spotify.com",
    "medal.tv",
    "www.medal.tv",
    "goo.gl",
    "spoti.fi",
    "discord.gg",
    "discord.com",
    "www.discord.com",
]

for domain in blacklist_domains:
    print(f"{timezone.now()} Creating BlackList domain {domain}")
    BlackList.objects.get_or_create(domain=domain)

# Delete all brands that have a blacklisted domain
print(f"{timezone.now()} Deleting brands with blacklisted domains")
blacklist_domains = BlackList.objects.values_list("domain", flat=True)
Brand.objects.filter(domain__in=blacklist_domains).delete()
