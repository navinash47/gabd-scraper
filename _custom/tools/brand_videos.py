from scrapper.models import Brand

# Take a domain as input
domain = "gearberry.com"
try:
    brand = Brand.objects.get(domain=domain)
    for deal in brand.brand_deals.all()[:10]:
        print("----------------------------------")
        print("https://www.youtube.com/watch?v=" + deal.video.video_id)
        print(deal.video.video_id, deal.video.title)

except Brand.DoesNotExist:
    print("Brand does not exist")
    exit()

# python manage.py shell < _custom/tools/brand_videos.py
