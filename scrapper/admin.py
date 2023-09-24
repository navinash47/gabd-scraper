from django.contrib import admin

from scrapper.models import Channel, Video, Brand, BrandDeal, BlackList

admin.site.register(Channel)
admin.site.register(Video)
admin.site.register(Brand)
admin.site.register(BrandDeal)
admin.site.register(BlackList)
