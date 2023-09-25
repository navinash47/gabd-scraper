import requests

from django.conf import settings
from django.utils import timezone

from scrapper.models import Channel, Video
from scrapper.utils import print_exception
from scrapper.limits import TOTAL_CHANNELS_COUNT


YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY

BATCH_SIZE = 50


# Use YouTube API to get details of a video
def _get_videos_details_yt_api(video_ids: list):
    if len(video_ids) > BATCH_SIZE:
        print_exception(f"{timezone.now()} VIDEOS Batch size is too large")
        raise Exception(f"{timezone.now()} VIDEOS Batch size is too large")

    base_url = f"https://youtube.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY,
    }
    headers = {"Accept": "application/json"}

    # Send the GET request
    response = requests.get(base_url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"{timezone.now()} YT Video Details successful")
        # You can access the response data using response.json()
        data = response.json()
        return data
    else:
        print(
            f"{timezone.now()} YT Video Details failed with status code: {response.status_code}"
        )
        return None


def _get_channels_details_yt_api(channel_ids: list):
    if len(channel_ids) > BATCH_SIZE:
        print_exception(f"{timezone.now()} CHANNELS Batch size is too large")
        raise Exception(f"{timezone.now()} CHANNELS Batch size is too large")

    base_url = f"https://youtube.googleapis.com/youtube/v3/channels"
    params = {
        "part": "snippet,statistics",
        "id": ",".join(channel_ids),
        "key": YOUTUBE_API_KEY,
    }
    headers = {"Accept": "application/json"}

    # Send the GET request
    response = requests.get(base_url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"{timezone.now()} YT Channel Details successful")
        # You can access the response data using response.json()
        data = response.json()
        return data
    else:
        print(
            f"{timezone.now()} YT Channel Details failed with status code: {response.status_code}"
        )
        return None


def get_videos_details(channel_ids):
    for channel_id in channel_ids:
        # If TOTAL_CHANNELS_COUNT number of channels ha
        if (
            Channel.objects.filter(status=Channel.COMPLETED).count()
            >= TOTAL_CHANNELS_COUNT
        ):
            # Don't scrape any more new channels
            print(f"{timezone.now()} Total channels count reached")
            return
        # Define the URL with parameters
        all_video_ids = list(
            Video.objects.filter(
                status=Video.SCRAPED, channel__channel_id=channel_id
            ).values_list("video_id", flat=True)
        )
        # Divide the video ids into batches of 50
        batches = [
            all_video_ids[i : i + BATCH_SIZE]
            for i in range(0, len(all_video_ids), BATCH_SIZE)
        ]
        for batch in batches:
            print(f"{timezone.now()} Getting video details for {channel_id}")
            data = _get_videos_details_yt_api(batch)
            if data is not None and "items" in data:
                for video_data in data["items"]:
                    video_id = video_data["id"]
                    print(f"{timezone.now()} Getting video details for {video_id}")
                    snippet = video_data["snippet"]
                    channel_id = snippet["channelId"]
                    channel = Channel.objects.get(channel_id=channel_id)
                    Video.objects.filter(video_id=video_id).update(
                        channel=channel,
                        title=snippet["title"],
                        thumbnail_url=snippet["thumbnails"]["default"]["url"],
                        description=snippet["description"],
                        default_language=snippet["defaultLanguage"]
                        if "defaultLanguage" in snippet
                        else None,
                        category_id=snippet["categoryId"],
                        published_at=snippet["publishedAt"],
                        # Statistics
                        view_count=video_data["statistics"]["viewCount"]
                        if "viewCount" in video_data["statistics"]
                        else 0,
                        like_count=video_data["statistics"]["likeCount"]
                        if "likeCount" in video_data["statistics"]
                        else 0,
                        favorite_count=video_data["statistics"]["favoriteCount"]
                        if "favoriteCount" in video_data["statistics"]
                        else 0,
                        comment_count=video_data["statistics"]["commentCount"]
                        if "commentCount" in video_data["statistics"]
                        else 0,
                        status=Video.DETAILED,
                        updated_at=timezone.now(),
                    )


def get_channels_details(channel_ids):
    batches = [
        channel_ids[i : i + BATCH_SIZE] for i in range(0, len(channel_ids), BATCH_SIZE)
    ]

    for batch in batches:
        print(f"{timezone.now()} Getting channel details for {batch} channels")
        data = _get_channels_details_yt_api(batch)
        if data is not None and "items" in data:
            for channel_data in data["items"]:
                channel_id = channel_data["id"]
                print(f"{timezone.now()} Getting channel details for {channel_id}")
                snippet = channel_data["snippet"]
                Channel.objects.update_or_create(
                    channel_id=channel_id,
                    defaults={
                        "title": snippet["title"],
                        "description": snippet["description"],
                        "custom_url": snippet["customUrl"]
                        if "customUrl" in snippet
                        else None,
                        "thumbnail_url": snippet["thumbnails"]["default"]["url"],
                        "country": snippet["country"] if "country" in snippet else None,
                        # Statistics
                        "view_count": channel_data["statistics"]["viewCount"],
                        "subscriber_count": channel_data["statistics"][
                            "subscriberCount"
                        ],
                        "hidden_subscriber_count": channel_data["statistics"][
                            "hiddenSubscriberCount"
                        ],
                        "video_count": channel_data["statistics"]["videoCount"],
                        "status": Channel.FETCHED,
                        "updated_at": timezone.now(),
                    },
                )


# DO NOT DELETE
video_sample = {
    "kind": "youtube#videoListResponse",
    "etag": "IijV52BN0AbJ--RsUa6ArtzIGkU",
    "items": [
        {
            "kind": "youtube#video",
            "etag": "pD37Go4PPbS3boVZbkT57QullGw",
            "id": "ILgSesWMUEI",
            "snippet": {
                "publishedAt": "2023-09-11T17:41:27Z",
                "channelId": "UCHnyfMqiRRG1u-2MsSQLbXA",
                "title": "All The Times We Nearly Blew Up The World",
                "description": "This is a video about some of the many times we have nearly blown up the world. Part of this video is brought to you by Henson -- head over to\nhttps://hensonshaving.com/veritasium and enter code 'Veritasium' for 100 free blades with the purchase of a razor. Make sure to add both the razor and the blades to your cart for the code to take effect. \n\n▀▀▀\nReferences:\nList of Broken Arrows -- https://ve42.co/AtomicArchive https://ve42.co/BrokenArrowsReport\nDeclassified Goldsboro Report -- https://ve42.co/Goldsboro\nOperation ChromeDome -- https://ve42.co/OperationChromeDome\nCIA website -- https://ve42.co/CIA\n\nCataclysmic cargo: The hunt for four missing nuclear bombs after a B-52 crash -- https://ve42.co/WoPo\nTHE LAST FLIGHT OF HOBO 28 -- https://ve42.co/lastflight\nThe Voice of Larry Messinger is from this documentary -- https://ve42.co/Messinger\nEven Without Detonation, 4 Hydrogen Bombs From ’66 Scar Spanish Village -- https://ve42.co/NYTPalomares\nDecades Later, Sickness Among Airmen After a Hydrogen Bomb Accident -- https://ve42.co/NYTPalomares2\nPicture of ReVelle -- https://ve42.co/JackReVelle1\nGreat NPR where the audio of ReVelle is from -- https://ve42.co/JackReVelle2\nCIA Website -- https://ve42.co/CIA\n\n\n▀▀▀\nSpecial thanks to our Patreon supporters:\nAnton Ragin, Balkrishna Heroor, Bernard McGee, Bill Linder, Burt Humburg, Dave Kircher, Diffbot, Evgeny Skvortsov, Gnare, Jesse Brandsoy, John H. Austin, Jr., john kiehl, Josh Hibschman, Juan Benet, KeyWestr, Lee Redden, Marinus Kuivenhoven, Mario Bottion, MaxPal, Meekay, meg noah, Michael Krugman, Orlando Bassotto, Paul Peijzel, Richard Sundvall, Sam Lutfi, Stephen Wilcox, Tj Steyn, TTST, Ubiquity Ventures\n\n▀▀▀\nDirected by Petr Lebedev\nWritten by Petr Lebedev and Derek Muller\nEdited by Peter Nelson\nAnimated by Fabio Albertelli, Jakub Misiek, Ivy Tello and Mike Radjabov\nFilmed by Derek Muller \nProduced by Petr Lebedev and Derek Muller\nAdditional video/photos supplied by Getty Images and Pond5\nMusic from Epidemic Sound",
                "thumbnails": {
                    "default": {
                        "url": "https://i.ytimg.com/vi/ILgSesWMUEI/default.jpg",
                        "width": 120,
                        "height": 90,
                    },
                    "medium": {
                        "url": "https://i.ytimg.com/vi/ILgSesWMUEI/mqdefault.jpg",
                        "width": 320,
                        "height": 180,
                    },
                    "high": {
                        "url": "https://i.ytimg.com/vi/ILgSesWMUEI/hqdefault.jpg",
                        "width": 480,
                        "height": 360,
                    },
                    "standard": {
                        "url": "https://i.ytimg.com/vi/ILgSesWMUEI/sddefault.jpg",
                        "width": 640,
                        "height": 480,
                    },
                    "maxres": {
                        "url": "https://i.ytimg.com/vi/ILgSesWMUEI/maxresdefault.jpg",
                        "width": 1280,
                        "height": 720,
                    },
                },
                "channelTitle": "Veritasium",
                "tags": ["veritasium", "science", "physics"],
                "categoryId": "27",
                "liveBroadcastContent": "none",
                "defaultLanguage": "en",
                "localized": {
                    "title": "All The Times We Nearly Blew Up The World",
                    "description": "This is a video about some of the many times we have nearly blown up the world. Part of this video is brought to you by Henson -- head over to\nhttps://hensonshaving.com/veritasium and enter code 'Veritasium' for 100 free blades with the purchase of a razor. Make sure to add both the razor and the blades to your cart for the code to take effect. \n\n▀▀▀\nReferences:\nList of Broken Arrows -- https://ve42.co/AtomicArchive https://ve42.co/BrokenArrowsReport\nDeclassified Goldsboro Report -- https://ve42.co/Goldsboro\nOperation ChromeDome -- https://ve42.co/OperationChromeDome\nCIA website -- https://ve42.co/CIA\n\nCataclysmic cargo: The hunt for four missing nuclear bombs after a B-52 crash -- https://ve42.co/WoPo\nTHE LAST FLIGHT OF HOBO 28 -- https://ve42.co/lastflight\nThe Voice of Larry Messinger is from this documentary -- https://ve42.co/Messinger\nEven Without Detonation, 4 Hydrogen Bombs From ’66 Scar Spanish Village -- https://ve42.co/NYTPalomares\nDecades Later, Sickness Among Airmen After a Hydrogen Bomb Accident -- https://ve42.co/NYTPalomares2\nPicture of ReVelle -- https://ve42.co/JackReVelle1\nGreat NPR where the audio of ReVelle is from -- https://ve42.co/JackReVelle2\nCIA Website -- https://ve42.co/CIA\n\n\n▀▀▀\nSpecial thanks to our Patreon supporters:\nAnton Ragin, Balkrishna Heroor, Bernard McGee, Bill Linder, Burt Humburg, Dave Kircher, Diffbot, Evgeny Skvortsov, Gnare, Jesse Brandsoy, John H. Austin, Jr., john kiehl, Josh Hibschman, Juan Benet, KeyWestr, Lee Redden, Marinus Kuivenhoven, Mario Bottion, MaxPal, Meekay, meg noah, Michael Krugman, Orlando Bassotto, Paul Peijzel, Richard Sundvall, Sam Lutfi, Stephen Wilcox, Tj Steyn, TTST, Ubiquity Ventures\n\n▀▀▀\nDirected by Petr Lebedev\nWritten by Petr Lebedev and Derek Muller\nEdited by Peter Nelson\nAnimated by Fabio Albertelli, Jakub Misiek, Ivy Tello and Mike Radjabov\nFilmed by Derek Muller \nProduced by Petr Lebedev and Derek Muller\nAdditional video/photos supplied by Getty Images and Pond5\nMusic from Epidemic Sound",
                },
                "defaultAudioLanguage": "en",
            },
            "statistics": {
                "viewCount": "1785455",
                "likeCount": "88117",
                "favoriteCount": "0",
                "commentCount": "3773",
            },
        }
    ],
    "pageInfo": {"totalResults": 1, "resultsPerPage": 1},
}


channel_sample = {
    "kind": "youtube#channelListResponse",
    "etag": "gruagsgpWy-D9YeUitHzppsMP3A",
    "pageInfo": {"totalResults": 1, "resultsPerPage": 5},
    "items": [
        {
            "kind": "youtube#channel",
            "etag": "R3WUkbv1nSl1lJkY658b9ystPxo",
            "id": "UCSHZKyawb77ixDdsGog4iWA",
            "snippet": {
                "title": "Lex Fridman",
                "description": "Lex Fridman Podcast and other videos.\n",
                "customUrl": "@lexfridman",
                "publishedAt": "2006-09-20T05:17:16Z",
                "thumbnails": {
                    "default": {
                        "url": "https://yt3.ggpht.com/ytc/AOPolaSfZCL-eF3cnKIkFToH-lB_ZvDOtwybuxVbhNkIGts=s88-c-k-c0x00ffffff-no-rj",
                        "width": 88,
                        "height": 88,
                    },
                    "medium": {
                        "url": "https://yt3.ggpht.com/ytc/AOPolaSfZCL-eF3cnKIkFToH-lB_ZvDOtwybuxVbhNkIGts=s240-c-k-c0x00ffffff-no-rj",
                        "width": 240,
                        "height": 240,
                    },
                    "high": {
                        "url": "https://yt3.ggpht.com/ytc/AOPolaSfZCL-eF3cnKIkFToH-lB_ZvDOtwybuxVbhNkIGts=s800-c-k-c0x00ffffff-no-rj",
                        "width": 800,
                        "height": 800,
                    },
                },
                "localized": {
                    "title": "Lex Fridman",
                    "description": "Lex Fridman Podcast and other videos.\n",
                },
                "country": "US",
            },
            "statistics": {
                "viewCount": "504387626",
                "subscriberCount": "3240000",
                "hiddenSubscriberCount": False,
                "videoCount": "780",
            },
        }
    ],
}
