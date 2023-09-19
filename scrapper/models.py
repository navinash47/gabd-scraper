import uuid
from django.db import models


class Channel(models.Model):
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

    updated_at = models.DateTimeField(auto_now=True)


class Video(models.Model):
    SCRAPED = "S"  # Got a video_id
    DETAILED = "D"  # Used YouTube API to get details
    FILTERED = "F"  # Used GPT-3 to filter brand deal links
    STATUS_CHOICES = [
        (SCRAPED, "Scraped"),
        (DETAILED, "Detailed"),
        (FILTERED, "Filtered"),
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

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=SCRAPED)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.video_id} - {self.title}"


class Brand(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    domain = models.CharField(max_length=200)
    name = models.CharField(max_length=200)


class BrandDeal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="brand_deals"
    )
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="brand_deals"
    )

    url = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)
