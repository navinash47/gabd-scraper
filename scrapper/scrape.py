from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrapper.models import Video


def scrape_video(video_url):
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


def scrape_channel(channel_url):
    prefix = "https://www.youtube.com/watch?v="

    # Configure Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Initialize Selenium webdriver
    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL
    driver.get(channel_url)

    # Extract all the videos from the channel
    try:
        element_xpath = "//*[@id='contents']"

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )

        while True:
            # Scroll down until id="spinner" disappears
            driver.execute_script(
                "window.scrollTo(0, document.getElementById('contents').scrollHeight);"
            )
            try:
                driver.find_element(By.ID, "spinner")
            except:
                print("END OF PAGE")
                break

        # Find the <a> elements with id="thumbnail"
        tb_elements = driver.find_elements(By.ID, "thumbnail")

        video_urls = []

        for tb_element in tb_elements:
            video_url = tb_element.get_attribute("href")
            if video_url is not None and video_url.startswith(prefix):
                video_urls.append(video_url)

        # Remove duplicates
        video_urls = list(set(video_urls))

        # Save the videos
        for video_url in video_urls:
            video_id = video_url[len(prefix) :]
            print(video_id)
            Video.objects.update_or_create(video_id=video_id)

        print(f"Found {len(video_urls)} videos")

    except Exception as e:
        print(e)

    finally:
        # Close the webdriver
        driver.quit()


channel_url = "https://www.youtube.com/@veritasium/videos"
scrape_channel(channel_url)
