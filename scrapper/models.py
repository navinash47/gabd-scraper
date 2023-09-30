import uuid
from django.db import models
from django.utils import timezone

from scrapper.utils import get_domain


class Channel(models.Model):
    CREATED = "C"  # Channel was created
    FETCHED = "F"  # Channel was fetched from YouTube API
    PROCESSING = "P"  # Video's are being scraped
    PAUSED = "A"  # New undetailed videos are added
    COMPLETED = "O"  # All videos have been scraped
    STATUS_CHOICES = [
        (CREATED, "Created"),
        (FETCHED, "Fetched"),
        (PROCESSING, "Processing"),
        (PAUSED, "Paused"),
        (COMPLETED, "Completed"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    channel_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    custom_url = models.CharField(max_length=200, null=True, blank=True)
    thumbnail_url = models.URLField(
        null=True, blank=True
    )  # In front end edit the url to get different resolutions - use medium or high
    country = models.CharField(max_length=200, null=True, blank=True)

    # Statistics
    view_count = models.BigIntegerField(default=0)
    subscriber_count = models.BigIntegerField(default=0)
    hidden_subscriber_count = models.BooleanField(default=False)
    video_count = models.BigIntegerField(default=0)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=CREATED)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel_id} - {self.title} - {self.status}"


class Video(models.Model):
    SCRAPED = "S"  # Got a video_id
    DETAILED = "D"  # Used YouTube API to get details
    FILTERED = "F"  # Used GPT-3 to filter brand deal links
    SKIPPED = "K"  # Skipped because of OPTIMIZATION in create_brand_deal_links
    STATUS_CHOICES = [
        (SCRAPED, "Scraped"),
        (DETAILED, "Detailed"),
        (FILTERED, "Filtered"),
        (SKIPPED, "Skipped"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="videos", null=True
    )
    created_at = models.DateTimeField(default=timezone.now)

    video_id = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    thumbnail_url = models.URLField(
        null=True, blank=True
    )  # In front end edit the url to get different resolutions - use medium or high
    description = models.TextField(null=True, blank=True)
    default_language = models.CharField(max_length=200, null=True, blank=True)
    category_id = models.CharField(max_length=200, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # Statistics
    view_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    favorite_count = models.BigIntegerField(default=0)
    comment_count = models.BigIntegerField(default=0)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=SCRAPED)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.video_id} {self.channel.title} - {self.status} - {self.title}"

    class Meta:
        ordering = ["-published_at"]


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    domain = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.domain}"

    # TODO create a validation function that checks if the domain is not blacklisted


class BrandDeal(models.Model):
    INITIAL = "I"  # The initial URL was scraped
    SCRAPED = "S"  # The final URL after all redirects was scraped
    STATUS_CHOICES = [
        (INITIAL, "Initial"),
        (SCRAPED, "Scraped"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="brand_deals", null=True
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="brand_deals"
    )
    created_at = models.DateTimeField(default=timezone.now)

    initial_url = models.TextField()
    final_url = models.TextField(null=True, blank=True)
    page_title = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INITIAL)
    updated_at = models.DateTimeField(auto_now=True)

    # video and initial_url should be unique together
    class Meta:
        unique_together = ["video", "initial_url"]

    def __str__(self):
        if self.final_url:
            return f"{self.video.channel.title} | {get_domain(self.initial_url)} | {get_domain(self.final_url)}"
        return f"{self.video.channel.title} | {get_domain(self.initial_url)}"


class BlackList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)

    domain = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f"{self.domain}"
