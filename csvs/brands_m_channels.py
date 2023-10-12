# Brands that have brand deals with more than 1 channel
import pandas as pd
from django.db.models import Count, Avg
from scrapper.models import BrandDeal, Channel

# Query the BrandDeal model to get brands with more than one channel
brands_with_multiple_channels = (
    BrandDeal.objects.values("brand__domain")
    .annotate(channel_count=Count("video__channel", distinct=True))
    .annotate(avg_subscriber_count=Avg("video__channel__subscriber_count"))
    .filter(channel_count__gt=2)
)

# Convert the query result to a pandas DataFrame
df = pd.DataFrame.from_records(brands_with_multiple_channels)

# Sort the DataFrame in descending order by channel_count
df = df.sort_values("avg_subscriber_count", ascending=False)

# Convert avg_subscriber_count to a readable string
df["avg_subscriber_count"] = df["avg_subscriber_count"].apply(
    lambda x: f"{x/1000:.1f} k" if x < 1000000 else f"{x/1000000:.1f} M"
)

# Save the DataFrame to a CSV file
df.to_csv("brands_with_multiple_channels.csv", index=False)
