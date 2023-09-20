import requests

from django.conf import settings
from django.utils import timezone

from scrapper.models import Channel, Video


YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY


# Use YouTube API to get details of a video
def get_video_details():
    # Define the URL with parameters
    all_video_ids = Video.objects.filter(status=Video.SCRAPED).values_list(
        "video_id", flat=True
    )[:50]
    print(len(all_video_ids))

    base_url = f"https://youtube.googleapis.com/youtube/v3/videos"

    params = {
        "part": "snippet,statistics",
        "id": ",".join(all_video_ids),
        "key": YOUTUBE_API_KEY,
    }

    # Define headers
    headers = {"Accept": "application/json"}

    # Send the GET request
    response = requests.get(base_url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request was successful")
        # You can access the response data using response.json()
        data = response.json()
        for video_data in data["items"]:
            video_id = video_data["id"]
            snippet = video_data["snippet"]
            channel_id = snippet["channelId"]
            channel, created = Channel.objects.get_or_create(channel_id=channel_id)
            Video.objects.filter(video_id=video_id).update(
                channel=channel,
                title=snippet["title"],
                description=snippet["description"],
                default_language=snippet["defaultLanguage"]
                if "defaultLanguage" in snippet
                else None,
                category_id=snippet["categoryId"],
                published_at=snippet["publishedAt"],
                # Statistics
                view_count=video_data["statistics"]["viewCount"],
                like_count=video_data["statistics"]["likeCount"],
                favorite_count=video_data["statistics"]["favoriteCount"],
                comment_count=video_data["statistics"]["commentCount"],
                status=Video.DETAILED,
                updated_at=timezone.now(),
            )
        return data
    else:
        print(f"Request failed with status code: {response.status_code}")


get_video_details()

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
            "etag": "DuGGebRw2ewH68GcombM8CyJv7U",
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
        }
    ],
}
