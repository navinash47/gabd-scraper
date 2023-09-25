from concurrent.futures import ThreadPoolExecutor

from django.utils import timezone

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapper.models import Brand, BrandDeal, BlackList
from scrapper.utils import get_domain, print_exception
from scrapper.limits import MAX_VALIDATE_WORKERS


VALIDATE_BATCH_SIZE = 50


def _get_final_details(chrome_options, initial_url):
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(initial_url)
        return driver.current_url, driver.title
    except Exception as e:
        log_string = (
            f"{timezone.now()} EXCEPTION in _get_final_details {initial_url}\n{e}"
        )
        print(log_string)
        print_exception(log_string)
        raise e
    finally:
        driver.quit()


def validate_brand_urls():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    try:
        brand_deals = BrandDeal.objects.filter(status=BrandDeal.INITIAL)
        batches = [
            brand_deals[i : i + VALIDATE_BATCH_SIZE]
            for i in range(0, len(brand_deals), VALIDATE_BATCH_SIZE)
        ]

        for batch in batches:
            futures_dict = {}
            with ThreadPoolExecutor(max_workers=MAX_VALIDATE_WORKERS) as executor:
                for brand_deal in batch:
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
                        print(
                            f"{timezone.now()} Already scraped {brand_deal.initial_url}"
                        )
                        brand_deal.brand = already_scraped.brand
                        brand_deal.final_url = already_scraped.final_url
                        brand_deal.page_title = already_scraped.page_title
                        brand_deal.status = BrandDeal.SCRAPED
                        brand_deal.save()
                        continue
                    futures_dict[brand_deal] = executor.submit(
                        _get_final_details, chrome_options, brand_deal.initial_url
                    )

                for brand_deal, future in futures_dict.items():
                    try:
                        final_url, page_title = future.result()
                        # Get the domain
                        domain = get_domain(final_url)
                        if domain:
                            # Get the brand
                            if BlackList.objects.filter(domain=domain).exists():
                                brand_deal.delete()
                                continue
                            brand, created = Brand.objects.get_or_create(domain=domain)
                            brand_deal.brand = brand
                        brand_deal.final_url = final_url
                        brand_deal.page_title = page_title
                        brand_deal.status = BrandDeal.SCRAPED
                        brand_deal.save()
                        print(
                            f"{timezone.now()} VALIDATED {brand_deal.initial_url} {brand_deal.final_url} {brand_deal.brand}"
                        )
                    except Exception as e:
                        brand_deal.status = BrandDeal.SCRAPED
                        brand_deal.save()
                        log_string = f"{timezone.now()} EXCEPTION in validate_brand_urls {brand_deal} {brand_deal.initial_url}\n{e}"
                        print(log_string)
                        print_exception(log_string)

    except Exception as e:
        log_string = f"{timezone.now()} EXCEPTION in validate_brand_urls OUTSIDE\n{e}"
        print(log_string)
        print_exception(log_string)
