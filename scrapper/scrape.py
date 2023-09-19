from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrapper.models import Video


def scrape_url(video_url):
    prefix = "https://www.youtube.com/watch?v="
    # Configure Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Initialize Selenium webdriver
    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL
    driver.get(video_url)

    try:
        element_xpath = "//ytd-compact-video-renderer"

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )

        # Find the <a> elements with id="thumbnail"
        tb_elements = driver.find_elements(By.ID, "thumbnail")

        # Print the links
        for tb_element in tb_elements:
            video_url = tb_element.get_attribute("href")
            if video_url is not None and video_url.startswith(prefix):
                video_id = video_url[len(prefix) :]
                print(video_id)
                Video.objects.update_or_create(video_id=video_id)

    except Exception as e:
        print(e)

    finally:
        # Close the webdriver
        driver.quit()


video_url = "https://www.youtube.com/watch?v=aGOV5R7M1Js"
scrape_url(video_url)
