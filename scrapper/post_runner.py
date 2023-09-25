from django.utils import timezone

from scrapper.limits import (
    TOTAL_CHANNELS_COUNT,
    CHANNEL_IGNORE_VIDEO_COUNT,
)
from scrapper.models import Channel, Video, Brand, BrandDeal, BlackList


print("----------------------------------------")
print(f"{timezone.now()} Total Channels: {Channel.objects.count()}")
print(f"{timezone.now()} Total Videos: {Video.objects.count()}")
print(f"{timezone.now()} Total Brands: {Brand.objects.count()}")
print(f"{timezone.now()} Total Brand Deals: {BrandDeal.objects.count()}")
print(f"{timezone.now()} Total BlackList: {BlackList.objects.count()}")
print("----------------------------------------")
print(f"{timezone.now()} TOTAL_CHANNELS_COUNT: {TOTAL_CHANNELS_COUNT}")
print(f"{timezone.now()} CHANNEL_IGNORE_VIDEO_COUNT: {CHANNEL_IGNORE_VIDEO_COUNT}")
