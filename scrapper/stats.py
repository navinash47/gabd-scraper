from scrapper.models import *

# Print the videos count with DETAILED status
print(
    f"Videos with DETAILED status: {Video.objects.filter(status=Video.DETAILED).count()}"
)

# Print the videos count with FILTERED status
print(
    f"Videos with FILTERED status: {Video.objects.filter(status=Video.FILTERED).count()}"
)

# Print the channels count
print(f"Channels count: {Channel.objects.count()}")

# Print the brands count
print(f"Brands count: {Brand.objects.count()}")

# Print the brand deals count
print(f"Brand deals count: {BrandDeal.objects.count()}")
