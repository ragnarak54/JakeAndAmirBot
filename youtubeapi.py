from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config

GOOGLE_API_KEY = config.google_api_key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def search(query):
    try:
        youtube = build(serviceName=YOUTUBE_API_SERVICE_NAME, version=YOUTUBE_API_VERSION, developerKey=GOOGLE_API_KEY)
        search_response = youtube.search().list(q=query, type="video", maxResults=1, part="id").execute()

        return "https://www.youtube.com/watch?v=" + search_response['items'][0]['id']['videoId']

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

    except KeyError:
        return "Could not find a video for this skit."
