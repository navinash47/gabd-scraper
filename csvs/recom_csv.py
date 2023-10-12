import csv
import uuid

import pandas as pd

from scrapper.models import Channel

# Load the uploaded CSV files
top_brands_per_channel_df = pd.read_csv("top_10_brands_per_channel.csv")
top_channels_per_brand_df = pd.read_csv("top_10_channels_per_brand.csv")

all_channel_ids = (
    top_brands_per_channel_df["channel_id"].unique().tolist()
    + top_channels_per_brand_df["channel_id"].unique().tolist()
)
all_brand_domains = (
    top_brands_per_channel_df["brand_domain"].unique().tolist()
    + top_channels_per_brand_df["brand_domain"].unique().tolist()
)

# Remove duplicates
all_channel_ids = list(set(all_channel_ids))
all_brand_domains = list(set(all_brand_domains))


# Helper function to write data to CSV
def write_to_csv(file_path, headers, data):
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


# Generating sample data for 'channels' table
channels_headers = [
    "id",
    "channel_id",
    "title",
    "custom_url",
    "thumbnail_url",
    "country",
    "view_count",
    "subscriber_count",
    "video_count",
]
channels_data = []
for channel_id in all_channel_ids:
    print(channel_id)
    channel = Channel.objects.get(channel_id=channel_id)
    channels_data.append(
        {
            "id": str(uuid.uuid4()),
            "channel_id": channel.channel_id,
            "title": channel.title,
            "custom_url": channel.custom_url,
            "thumbnail_url": channel.thumbnail_url,
            "country": channel.country,
            "view_count": channel.view_count,
            "subscriber_count": channel.subscriber_count,
            "video_count": channel.video_count,
        }
    )


# Generating sample data for 'brands' table
brands_headers = ["id", "domain"]
brands_data = []
for brand_domain in all_brand_domains:
    print(brand_domain)
    brands_data.append(
        {
            "id": str(uuid.uuid4()),
            "domain": brand_domain,
        }
    )

# Write to CSV files
write_to_csv("csvs/results/channels.csv", channels_headers, channels_data)
write_to_csv("csvs/results/brands.csv", brands_headers, brands_data)
