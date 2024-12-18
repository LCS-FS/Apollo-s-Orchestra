import pylast
import requests

# API credentials
API_KEY = "c392fa71288487f885a6b34d375c4cc4"  
API_SECRET = "c377a9bf09e4a6b47a98b8d22088d1c8"

# Authenticate
username = "apolloestra"
password_hash = pylast.md5("Apollo911!")

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)


def get_album_cover(mbid):
    # Parameters for the API request
    BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

    params = {
        'method': 'album.getinfo',
        'api_key': API_KEY,
        'mbid': mbid,
        'format': 'json'
    }
    
    # Make the API request
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    
    # Check if the response contains the album info
    if 'album' in data and 'image' in data['album']:
        # Extract the URL of the largest image (usually the last one in the list)
        images = data['album']['image']
        if images:
            cover_url = images[-1]['#text']  # The largest size is typically at the end
            return cover_url
        else:
            return None
    else:
        return None

def search_track_by_mbid(mbid):
    return network.get_track_by_mbid(mbid)

def search_artist_by_mbid(mbid):
    return network.get_artist_by_mbid(mbid)

def search_album_by_mbid(mbid):
    return network.get_album_by_mbid(mbid)