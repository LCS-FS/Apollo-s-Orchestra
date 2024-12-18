from django.shortcuts import render
from django.http import HttpResponse
from .fetch import fetch_album, fetch_album_from_id, fetch_artist_from_id, fetch_artist, fetch_track, fetch_track_from_id, join_album_tracks, join_artist_albums
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, "index.html", {"query": "", "type": 0})

def search(request):
    query = request.GET.get("query")
    searchType = request.GET.get("searchType")
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
    return render(request, "search.html", {"results": results, "type": searchType, "query": query, "type": typeNum})

def get_artist(request, artist_id):
    artist = fetch_artist_from_id(artist_id)
    artist_with_albums = join_artist_albums(artist)
    try:
        # Convert artist_obj to an RDF graph
        g = artist_with_albums.to_rdf()

        # Print the graph in Turtle format
        print("Serialized RDF Graph in Turtle format:")
        print(g.serialize(format="turtle"))
    except Exception as e:
        g = None
        print(f"Error while serializing RDF graph: {e}")
    return artist_with_albums, g

def get_album(request, album_id):
    album = fetch_album_from_id(album_id)
    album_with_tracks = join_album_tracks(album)
    try:
        # Convert artist_obj to an RDF graph
        g = album_with_tracks.to_rdf()

        # Print the graph in Turtle format
        print("Serialized RDF Graph in Turtle format:")
        print(g.serialize(format="turtle"))
    except Exception as e:
        g = None
        print(f"Error while serializing RDF graph: {e}")
    return album_with_tracks, g

def get_track(request, track_id):
    track = fetch_track_from_id(track_id)
    try:
        # Convert artist_obj to an RDF graph
        g = track.to_rdf()

        # Print the graph in Turtle format
        print("Serialized RDF Graph in Turtle format:")
        print(g.serialize(format="turtle"))
    except Exception as e:
        g = None
        print(f"Error while serializing RDF graph: {e}")
    return track, g

def artist(request, artist_id):
    artist_with_albums, g = get_artist(request, artist_id)
    return render(request, "main_pages/artist.html", {"artist": artist_with_albums, "graph": g.serialize(format="turtle")})

def album(request, album_id):
    album_with_tracks, g = get_album(request, album_id)
    return render(request, "main_pages/album.html", {"album": album_with_tracks, "graph": g.serialize(format="turtle")})

def track(request, track_id):
    track, g = get_track(request, track_id)
    return render(request, "main_pages/track.html", {"track": track, "graph": g.serialize(format="turtle")})

def artist_api(request, artist_id):
    _, g = get_artist(request, artist_id)

    data = {
        "graph": g.serialize(format="turtle") if g else None
    }
    return JsonResponse(data)

def album_api(request, album_id):
    _, g = get_album(request, album_id)

    data = {
        "rdf": g.serialize(format="turtle") if g else None
    }
    return JsonResponse(data)

def track_api(request, track_id):
    _, g = get_track(request, track_id)

    data = {
        "rdf": g.serialize(format="turtle") if g else None
    }
    return JsonResponse(data)