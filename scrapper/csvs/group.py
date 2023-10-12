import csv
from django.db.models import Count
from scrapper.models import BrandDeal

from scrapper.csvs.utils import accept_domain


# Step 2: Create QuerySet
deals_count_query = (
    BrandDeal.objects.values(
        "video__channel__channel_id",
        "video__channel__title",
        "video__channel__country",
        "video__channel__view_count",
        "video__channel__subscriber_count",
        "video__channel__video_count",
        "brand__domain",
    )
    .annotate(deals_count=Count("id"))
    .order_by("video__channel", "-deals_count", "brand")
)

# Step 3: Open a TSV file for writing
with open("c_bd.tsv", "w", newline="") as tsvfile:
    # Step 4: Write the header row
    writer = csv.writer(tsvfile, delimiter="\t")
    writer.writerow(
        [
            "channel_id",
            "channel_title",
            "brand_domain",
            "deals_count",
            "country",
            "view_count",
            "subscriber_count",
            "video_count",
        ]
    )

    # Step 5: Loop through the QuerySet
    for record in deals_count_query:
        channel_id = record["video__channel__channel_id"]
        channel_title = record["video__channel__title"]
        brand_domain = record["brand__domain"]
        deals_count = record["deals_count"]
        country = record["video__channel__country"]
        view_count = record["video__channel__view_count"]
        subscriber_count = record["video__channel__subscriber_count"]
        video_count = record["video__channel__video_count"]

        if not brand_domain or not accept_domain(brand_domain):
            continue

        # Write to TSV
        writer.writerow(
            [
                channel_id,
                channel_title,
                brand_domain,
                deals_count,
                country,
                view_count,
                subscriber_count,
                video_count,
            ]
        )
