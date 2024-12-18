from django.shortcuts import render
from django.http import HttpResponse
from .fetch import fetch_album, fetch_album_from_id, fetch_artist_from_id, fetch_artist, fetch_track, fetch_track_from_id, join_album_tracks, join_artist_albums

# Create your views here.
def index(request):
    return render(request, "index.html", {"query": "", "type": 0})

def search(request):
    query = request.GET.get("query")
    searchType = request.GET.get("searchType")
    
    print(query)
    print(searchType)

    match searchType:
        case "artists":
            results = fetch_artist(query)
            typeNum = 1
        case "albums":
            results = fetch_album(query)
            typeNum = 2
        case "tracks":
            results = fetch_track(query)
            typeNum = 3
        case _:
            typeNum = 0
            results = []
        
    results = sorted(results)
    print(results)
    return render(request, "search.html", {"results": results, "type": searchType, "query": query, "type": typeNum})

def artist(request, artist_id):
    artist = fetch_artist_from_id(artist_id)
    artist_with_albums = join_artist_albums(artist)
    return render(request, "main_pages/artist.html", {"artist": artist_with_albums})

def album(request, album_id):
    album = fetch_album_from_id(album_id)
    album_with_tracks = join_album_tracks(album)
    return render(request, "main_pages/album.html", {"album": album_with_tracks})

def track(request, track_id):
    track = fetch_track_from_id(track_id)
    return render(request, "main_pages/track.html", {"track": track})

def artist_rdf(request, artist_id):
    artist = fetch_artist_from_id(artist_id)
    print(artist)
    artist_with_albums = join_artist_albums(artist)

    result = artist_with_albums.to_rdf()
    print(result)
    return render(request, "artist.html", {"result": result})

def album_rdf(request, album_id):
    album = fetch_album_from_id(album_id)
    album_with_tracks = join_album_tracks(album)

    result = album_with_tracks.to_rdf()
    return render(request, "album.html", {"result": result})

def track_rdf(request, track_id):
    track = fetch_track_from_id(track_id)
    result = track.to_rdf()
    return render(request, "track.html", {"result": result})