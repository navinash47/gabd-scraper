import re

from django.utils import timezone

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapper.models import Brand, BrandDeal


def validate_brand_urls():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    try:
        # Initialize Selenium webdriver
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(30)  # seconds
        brand_deals = BrandDeal.objects.filter(status=BrandDeal.INITIAL)

        for brand_deal in brand_deals:
            try:
                # Navigate to the short URL
                print("--------------------------")
                print(
                    f"{timezone.now()} Validating brand deal initial URL {brand_deal.initial_url}",
                )
                # If a brand deal has already been scraped, skip it
                already_scraped = BrandDeal.objects.filter(
                    initial_url=brand_deal.initial_url, status=BrandDeal.SCRAPED
                ).first()
                if already_scraped:
                    print(f"{timezone.now()} Already scraped {brand_deal.initial_url}")
                    brand_deal.brand = already_scraped.brand
                    brand_deal.final_url = already_scraped.final_url
                    brand_deal.status = BrandDeal.SCRAPED
                    brand_deal.save()
                    continue
                driver.get(brand_deal.initial_url)
                # Get the final URL after all redirects
                final_url = driver.current_url
                print(f"{timezone.now()} Final URL {final_url}")
                # Get the domain name
                domain_regex = r"(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n]+)"
                domain = re.search(domain_regex, final_url).group(1)
                print(f"{timezone.now()} Domain {domain}")
                # Create a Brand object if it doesn't exist
                brand, created = Brand.objects.get_or_create(domain=domain)
                # Update the brand deal
                brand_deal.brand = brand
                brand_deal.final_url = final_url
                brand_deal.status = BrandDeal.SCRAPED
                brand_deal.save()

            except Exception as e:
                brand_deal.status = BrandDeal.SCRAPED
                brand_deal.save()
                print(
                    f"{timezone.now()} EXCEPTION in validate_brand_urls {brand_deal} INSIDE"
                )
                print(e)

    except Exception as e:
        print(f"{timezone.now()} EXCEPTION in validate_brand_urls OUTSIDE")
        print(e)

    finally:
        # Close the WebDriver
        driver.quit()


validate_brand_urls()
