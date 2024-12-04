import pylast

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

# Get a track
track = network.get_track("Iron Maiden", "The Nomad")

# Fetch and display more details about the track
print(f"Track: {track.get_title()}")
print(f"Artist: {track.get_artist()}")
print(f"Album: {track.get_album()}")
print(f"Duration (ms): {track.get_duration()}")
print(f"Play Count: {track.get_playcount()}")
print(f"Listeners: {track.get_listener_count()}")
print(f"Tags: {', '.join(tag.item for tag in track.get_top_tags(limit=5))}")
print(f"Wiki Summary: {track.get_wiki_summary()}")
print(f"Wiki Content: {track.get_wiki_content()}")