import os
import re
import openai
import backoff

from scrapper.models import Video, BrandDeal

openai.api_key = os.getenv("OPENAI_API_KEY")


# Use GPT-3.5 and extract brand deal links
system_prompt = "You help extract brand deal or sponsored segment links"
user_prompt = """
Brand Deals are sponsored segments where a YouTuber shares endorses brands by sharing a discounted URL to the brands product or service.  
The following is a YouTube description. It may contain 0-6 brand deals.
Extract the section that contains the brand deal/deals. If there is no brand deal, return "".
Here's the description
'''
{description}
'''
"""


# 3,500 RPM - Paid users after 48 hours
# https://platform.openai.com/docs/guides/rate-limits/overview
@backoff.on_exception(backoff.expo, openai.error.RateLimitError)  # TODO test
def extract_brand_deal_links(description):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt.format(description=description),
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    brand_deals_section = response.choices[0]["message"]["content"]
    # Extract urls from the section using regex
    urls = re.findall(r"(?P<url>https?://[^\s]+)", brand_deals_section) or [""]
    # Remove all "" strings
    urls = [url for url in urls if url]
    return urls


def create_brand_deal_links():
    detailed_videos = Video.objects.filter(
        status=Video.DETAILED,
    )
    BATCH_SIZE = 100
    batches = [
        detailed_videos[i : i + BATCH_SIZE]
        for i in range(0, len(detailed_videos), BATCH_SIZE)
    ]
    for batch in batches:
        for video in batch:
            print("Extracting brand deal links for", video.video_id)
            urls = extract_brand_deal_links(
                video.description[:2000]
            )  # The first 2000 characters
            # Remove duplicates
            urls = list(set(urls))
            print(video.video_id, urls)
            BrandDeal.objects.bulk_create(
                [BrandDeal(video=video, initial_url=url) for url in urls]
            )
