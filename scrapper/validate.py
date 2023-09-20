from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapper.models import Brand, BrandDeal


def validate_brand_urls():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Initialize Selenium webdriver
    driver = webdriver.Chrome(options=chrome_options)
    try:
        initial_urls = BrandDeal.objects.filter(status=BrandDeal.INITIAL).values_list(
            "initial_url", flat=True
        )

        for initial_url in initial_urls:
            # Navigate to the short URL
            driver.get(initial_url)
            # Get the final URL after all redirects
            final_url = driver.current_url
            # Get the domain name
            domain = final_url.split("/")[2]
            # Create a Brand object if it doesn't exist
            brand, created = Brand.objects.get_or_create(domain=domain)
            BrandDeal.objects.filter(initial_url=initial_url).update(
                brand=brand,
                final_url=final_url,
                status=BrandDeal.SCRAPED,
            )

    except Exception as e:
        print(e)

    finally:
        # Close the WebDriver
        driver.quit()
