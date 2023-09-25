from django.db.models import Q
from django.utils import timezone


from scrapper.models import Channel
from scrapper.scrape import scrape_new_channels, scrape_channels_videos
from scrapper.details import get_videos_details
from scrapper.filter import create_brand_deal_links
from scrapper.validate import validate_brand_urls
from scrapper.limits import TOTAL_CHANNELS_COUNT
from scrapper.utils import print_exception


def get_channels_pipeline():
    if Channel.objects.count() >= TOTAL_CHANNELS_COUNT:
        # Don't scrape any more new channels
        print(f"{timezone.now()} Total channels count reached")
        return
    print(f"{timezone.now()} Getting new channels")
    # Get one video from every channel
    channels = Channel.objects.filter(status=Channel.FETCHED).order_by("created_at")
    print(
        f"{timezone.now()} Cross scraping {channels.count()} channels for new channels"
    )
    for channel in channels:
        video = channel.videos.first()
        if video is not None:
            scrape_new_channels(video.video_id)


def get_video_details_pipeline():
    print(f"{timezone.now()} Getting video details")
    channel_ids = list(
        Channel.objects.filter(Q(status=Channel.FETCHED) | Q(status=Channel.PAUSED))
        .order_by("-updated_at")
        .values_list("channel_id", flat=True)
    )
    # Change the status of the channels to PROCESSING
    Channel.objects.filter(channel_id__in=channel_ids).update(status=Channel.PROCESSING)
    try:
        scrape_channels_videos(channel_ids)
        get_videos_details(channel_ids)
        Channel.objects.filter(channel_id__in=channel_ids).update(
            status=Channel.COMPLETED
        )
    except Exception as e:
        print(f"{timezone.now()} Error in getting video details CYCLE")
        print(e)
        print_exception(f"{timezone.now()} Error in getting video details CYCLE\n{e}")
        Channel.objects.filter(channel_id__in=channel_ids).update(status=Channel.PAUSED)


def get_brand_deals_pipeline():
    print(f"{timezone.now()} Getting brand deals")
    create_brand_deal_links()


def validate_brand_deals_pipeline():
    print(f"{timezone.now()} Validating brand deals")
    validate_brand_urls()
