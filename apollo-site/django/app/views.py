from django.shortcuts import render
from django.http import HttpResponse
from fetch import fetch_artist_from_id, fetch_artist

# Create your views here.
def index(request):
    return render(request, "index.html")

def search(request):
    query = request.GET.get("q")
    results = fetch_artist(query)

    return render(request, "search.html", {"results": results})

def artist(request, artist_id):
    artist = fetch_artist_from_id(artist_id)

    return render(request, "artist.html", {"artist": artist, "albums": albums})