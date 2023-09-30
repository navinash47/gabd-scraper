import csv
from scrapper.models import BrandDeal

from scrapper.csvs.utils import ignore_brand_domains

# Step 2: Create the QuerySet
brand_deals = BrandDeal.objects.select_related("brand", "video", "video__channel").all()

# Step 3: Open a TSV file for writing
with open("bd.tsv", "w", newline="") as tsvfile:
    # Step 4: Write the header row
    writer = csv.writer(tsvfile, delimiter="\t")
    writer.writerow(
        [
            "channel_id",
            "channel_title",
            "brand_domain",
            "video_id",
            "published_at",
            "brand_initial_link",
            "brand_final_link",
        ]
    )

    # Step 5: Loop through the QuerySet
    for deal in brand_deals:
        channel_id = deal.video.channel.channel_id
        channel_title = deal.video.channel.title
        brand_domain = deal.brand.domain
        video_id = deal.video.video_id
        published_at = deal.video.published_at
        brand_initial_link = deal.initial_url
        brand_final_link = deal.final_url

        if not brand_domain or brand_domain in ignore_brand_domains:
            continue

        # Write to TSV
        writer.writerow(
            [
                channel_id,
                channel_title,
                brand_domain,
                video_id,
                published_at,
                brand_initial_link,
                brand_final_link,
            ]
        )
