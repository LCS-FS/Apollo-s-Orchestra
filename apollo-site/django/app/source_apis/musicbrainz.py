import musicbrainzngs as mb

mb.set_useragent("apollo", "0.1", "http://localhost:8000")

def search_artist(query):
    return mb.search_artists(artist=query)