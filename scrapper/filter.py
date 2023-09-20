import os
import ast
import openai

from scrapper.models import Video, BrandDeal

openai.api_key = os.getenv("OPENAI_API_KEY")

# TODO this doesn't seem to work reliably. Sometimes it returns the wrong links - ['http://bit.ly/100Wk2K', 'http://bit.ly/TV3xO5', 'http://bit.ly/11upebY']
# Think of a better way to do this

# Use GPT-3.5 and extract brand deal links
system_prompt = "You help extract brand deal or sponsored segment links"
user_prompt = """
The following is a YouTube description. Please extract the brand deal or sponsored segment link from the description. Return a JSON that has a "url" key.
Here's the description
'''
{description}
'''
"""


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
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    urls_str = response.choices[0]["message"]["content"]
    # Convert to list
    urls = ast.literal_eval(urls_str)
    return urls["url"]


# TODO rate limit
def create_brand_deal_links():
    detailed_videos = Video.objects.filter(status=Video.DETAILED)[:10]
    for video in detailed_videos:
        url = extract_brand_deal_links(video.description)
        print(video.video_id, url)
        BrandDeal.objects.get_or_create(video=video, initial_url=url)


create_brand_deal_links()
