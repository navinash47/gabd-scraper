from django.db.models.signals import post_save
from django.dispatch import receiver

from scrapper.models import BlackList, Brand


@receiver(post_save, sender=BlackList)
def delete_brands_with_blacklisted_domain(sender, instance, **kwargs):
    Brand.objects.filter(domain=instance.domain).delete()
