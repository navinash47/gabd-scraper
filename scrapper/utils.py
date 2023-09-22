from scrapper.models import Channel
from scrapper.details import get_channels_details

test_channel_ids = [
    "UCSHZKyawb77ixDdsGog4iWA",  # Lex Fridman
    "UCHnyfMqiRRG1u-2MsSQLbXA",  # Veritasium
]

print("Creating test channels")
get_channels_details(test_channel_ids)
