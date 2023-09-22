from django.db.models import Q


from scrapper.models import Channel
from scrapper.scrape import scrape_new_channels, scrape_channels_videos
from scrapper.details import get_videos_details
from scrapper.filter import create_brand_deal_links
from scrapper.validate import validate_brand_urls
from scrapper.limits import TOTAL_CHANNELS_COUNT

CYCLES = 10


def get_channels_pipeline():
    if Channel.objects.count() >= TOTAL_CHANNELS_COUNT:
        # Don't scrape any more new channels
        return
    for i in range(CYCLES):
        print("Getting channels CYCLE", i)
        # Get one video from every channel
        channels = Channel.objects.filter(
            has_cross_scraped=False, status=Channel.FETCHED
        ).order_by("-created_at")
        for channel in channels:
            video = channel.videos.first()
            if video is not None:
                scrape_new_channels(video.video_id)
                channel.has_cross_scraped = True
                channel.save(update_fields=["has_cross_scraped"])


def get_video_details_pipeline():
    for i in range(CYCLES):
        print("Getting video details CYCLE", i)
        channel_ids = list(
            Channel.objects.filter(Q(status=Channel.FETCHED) | Q(status=Channel.PAUSED))
            .order_by("-updated_at")
            .values_list("channel_id", flat=True)
        )
        # Change the status of the channels to PROCESSING
        Channel.objects.filter(channel_id__in=channel_ids).update(
            status=Channel.PROCESSING
        )
        try:
            scrape_channels_videos(channel_ids)
            get_videos_details(channel_ids)
            Channel.objects.filter(channel_id__in=channel_ids).update(
                status=Channel.COMPLETED
            )
        except Exception as e:
            print("Exception in get_video_details_pipeline")
            print(e)
            Channel.objects.filter(channel_id__in=channel_ids).update(
                status=Channel.PAUSED
            )


def get_brand_deals_pipeline():
    for i in range(CYCLES):
        print("Filtering brand deals CYCLE", i)
        create_brand_deal_links()


def validate_brand_deals_pipeline():
    for i in range(CYCLES):
        print("Validating brand deals CYCLE", i)
        validate_brand_urls()
