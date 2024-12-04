import requests

def get_lyrics(artist_name, track_name):
    base_url = f"https://api.lyrics.ovh/v1/{artist_name}/{track_name}"
    response = requests.get(base_url)
    
    if response.status_code != 200:
        return f"Error: Unable to fetch lyrics. Status code: {response.status_code}"
    
    data = response.json()
    lyrics = data.get("lyrics", "")
    if not lyrics:
        return "Lyrics not found."
    
    return lyrics.strip()

# Example usage
artist = "Iron Maiden"
track = "The Nomad"
lyrics = get_lyrics(artist, track)
print(f"Lyrics for '{track}' by {artist}:\n{lyrics}")