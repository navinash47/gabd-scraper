from django.utils import timezone
from django.db.models import Q

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrapper.models import Video, Channel
from scrapper.details import _get_videos_details_yt_api, get_channels_details
from scrapper.limits import CHANNEL_IGNORE_VIDEO_COUNT


def scrape_new_channels(root_video_id: str):
    prefix = "https://www.youtube.com/watch?v="
    # Configure Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Initialize Selenium webdriver
    driver = webdriver.Chrome(options=chrome_options)

    # Open the URL
    root_video_url = f"{prefix}{root_video_id}"
    driver.get(root_video_url)

    try:
        print(f"{timezone.now()} Scraping CROSS - video with id", root_video_id)
        element_xpath = "//ytd-compact-video-renderer"

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )

        # Find the <a> elements with id="thumbnail"
        tb_elements = driver.find_elements(By.ID, "thumbnail")

        # Print the links
        video_ids = []
        for tb_element in tb_elements:
            video_url = tb_element.get_attribute("href")
            if video_url is not None and video_url.startswith(prefix):
                video_id = video_url[len(prefix) :]
                video_ids.append(video_id)

        # Remove duplicates
        video_ids = list(set(video_ids))
        print(f"{timezone.now()} Found CROSS SCRAPED videos", len(video_ids))
        # Use YouTube API to get the details of the videos
        BATCH_SIZE = 50
        batches = [
            video_ids[i : i + BATCH_SIZE] for i in range(0, len(video_ids), BATCH_SIZE)
        ]
        channels_set = set()
        for batch in batches:
            data = _get_videos_details_yt_api(batch)
            if data is not None and "items" in data:
                channel_ids = [video["snippet"]["channelId"] for video in data["items"]]
                channels_set.update(channel_ids)

        channels_list = list(channels_set)
        get_channels_details(channels_list)

    except Exception as e:
        print("Exception in scrape_new_channels")
        print(e)

    finally:
        # Close the webdriver
        driver.quit()


def _get_video_ids(driver, prefix: str):
    tb_elements = driver.find_elements(By.ID, "thumbnail")
    video_urls = []
    for tb_element in tb_elements:
        video_url = tb_element.get_attribute("href")
        if video_url is not None and video_url.startswith(prefix):
            video_urls.append(video_url)

    # Remove duplicates
    video_urls = list(set(video_urls))

    return video_urls


def scrape_channels_videos(channel_ids: list):
    # Channels that have status INITIALISED
    prefix = "https://www.youtube.com/watch?v="

    # Configure Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Initialize Selenium webdriver
    driver = webdriver.Chrome(options=chrome_options)

    # Extract all the videos from the channel
    try:
        for channel_id in channel_ids:
            try:
                print(f"{timezone.now()} Scraping channel with id", channel_id)
                channel = Channel.objects.get(
                    channel_id=channel_id, status=Channel.PROCESSING
                )
                if channel is None or channel.video_count > CHANNEL_IGNORE_VIDEO_COUNT:
                    print(
                        f"{timezone.now()} SKIPPING channel {channel.title} that has {channel.video_count} videos"
                    )
                    continue

                print(
                    f"{timezone.now()} SCRAPING channel {channel.title} that has {channel.video_count} videos"
                )
                channel.status = Channel.PROCESSING
                channel.save(update_fields=["status"])
                channel_url = f"https://www.youtube.com/channel/{channel_id}/videos"
                # Open the URL
                driver.get(channel_url)
                element_xpath = "//*[@id='contents']"

                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, element_xpath))
                )

                print("PRECHECK OF VIDEOS")
                video_urls = _get_video_ids(driver, prefix)
                video_ids = [video_url[len(prefix) :] for video_url in video_urls]
                # Check if all the videos have been scraped
                if Video.objects.filter(video_id__in=video_ids).count() > 1:
                    # Save the videos
                    update_channel = False
                    for video_id in video_ids:
                        video, created = Video.objects.get_or_create(
                            video_id=video_id, defaults={"channel": channel}
                        )
                        if created:
                            update_channel = True
                    print("ALL VIDEOS HAVE BEEN SCRAPED")
                    if update_channel:
                        channel.status = Channel.PAUSED
                        channel.save(update_fields=["status"])
                    continue
                print("SCROLLING DOWN")

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

                video_urls = _get_video_ids(driver, prefix)

                # Save the videos
                for video_url in video_urls:
                    video_id = video_url[len(prefix) :]
                    Video.objects.get_or_create(
                        video_id=video_id, defaults={"channel": channel}
                    )

                channel.status = Channel.PAUSED
                channel.save(update_fields=["status"])

                print(
                    f"{timezone.now()} SCRAPED channel {channel.title} that has {channel.video_count} videos"
                )

            except Exception as e:
                print("Exception in scrape_channels_videos INSIDE")
                print(e)

    except Exception as e:
        print("Exception in scrape_channels_videos OUTSIDE")
        print(e)

    finally:
        # Close the webdriver
        driver.quit()
