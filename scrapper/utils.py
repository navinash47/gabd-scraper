from django.utils import timezone

from scrapper.details import get_channels_details

test_channel_ids = [
    "UCSHZKyawb77ixDdsGog4iWA",  # Lex Fridman
    "UCHnyfMqiRRG1u-2MsSQLbXA",  # Veritasium
]

print(f"{timezone.now()} Creating test channels")
get_channels_details(test_channel_ids)
