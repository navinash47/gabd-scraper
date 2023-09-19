import uuid
from django.db import models


class Channel(models.Model):
    INITIALZED = "I"
    SCRAPING = "S"
    SCRAPED = "D"
    FAILED = "F"
    STATUS_CHOICES = [
        (INITIALZED, "Initialized"),
        (SCRAPING, "Scraping"),
        (SCRAPED, "Scraped"),
        (FAILED, "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    channel_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    custom_url = models.URLField(null=True, blank=True)
    default_language = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    # Statistics
    view_count = models.BigIntegerField(default=0)
    subscriber_count = models.BigIntegerField(default=0)
    hidden_subscriber_count = models.BooleanField(default=False)
    video_count = models.BigIntegerField(default=0)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INITIALZED)
    updated_at = models.DateTimeField(auto_now=True)


class Video(models.Model):
    INITIALZED = "I"
    SCRAPING = "S"
    SCRAPED = "D"
    FAILED = "F"
    STATUS_CHOICES = [
        (INITIALZED, "Initialized"),
        (SCRAPING, "Scraping"),
        (SCRAPED, "Scraped"),
        (FAILED, "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="videos", null=True
    )

    video_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    default_language = models.CharField(max_length=200, null=True, blank=True)
    category_id = models.CharField(max_length=200, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # Statistics
    view_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    dislike_count = models.BigIntegerField(default=0)
    favorite_count = models.BigIntegerField(default=0)
    comment_count = models.BigIntegerField(default=0)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INITIALZED)
    updated_at = models.DateTimeField(auto_now=True)


class BrandDealLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="brand_deal_links"
    )

    url = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)
