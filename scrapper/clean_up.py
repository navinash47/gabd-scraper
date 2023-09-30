import re
from django.utils import timezone

from scrapper.models import BrandDeal, Brand, BlackList, Video
from scrapper.utils import get_domain

print(f"{timezone.now()} Deleting all BrandDeal objects with incomplete data")
for brand in Brand.objects.all():
    # Incomplete brand domain
    domain = brand.domain
    if len(domain.split(".")) < 2:
        brand.delete()

for brand_deal in BrandDeal.objects.all():
    # Incomplete brand deal initial_url or blacklisted
    initial_url = brand_deal.initial_url
    domain = get_domain(initial_url)
    if len(domain.split(".")) < 2 or BlackList.objects.filter(domain=domain).exists():
        print("--------------------")
        print(domain)
        print(initial_url)
        brand_deal.delete()


# Delete all brands that have a blacklisted domain
print(f"{timezone.now()} Deleting brands with blacklisted domains")
blacklist_domains = BlackList.objects.values_list("domain", flat=True)
Brand.objects.filter(domain__in=blacklist_domains).delete()

# Delete all domains that end with .
print(f"{timezone.now()} Deleting brands with domains that end with .")
Brand.objects.filter(domain__endswith=".").delete()

# # Get all urls from the videos description. If a brand deal's initial_url doesn't appear in the description, delete it
# print(
#     f"{timezone.now()} Deleting brand deals with urls that don't appear in the description"
# )
# for brand_deal in BrandDeal.objects.all():
#     video = brand_deal.video
#     description = video.description
#     all_urls = re.findall(r"(?P<url>https?://[^\s]+)", description)
#     if brand_deal.initial_url not in all_urls:
#         print(
#             f"{timezone.now()} Deleting brand deal {brand_deal.initial_url} for video {video.video_id}"
#         )
#         # brand_deal.delete()

# # Change Video with no brand deals but with FILTERED status to DETAILED
# print(
#     f"{timezone.now()} Changing Video with no brand deals but with FILTERED status to DETAILED"
# )
# queryset = Video.objects.filter(brand_deals__isnull=True, status=Video.FILTERED).update(
#     status=Video.DETAILED
# )
