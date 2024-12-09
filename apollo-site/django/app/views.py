from django.shortcuts import render
from django.http import HttpResponse
from .source_apis import musicbrainz as mb

# Create your views here.
def index(request):
    return render(request, "index.html")

def search(request):
    query = request.GET.get("q")
    results = mb.search_artist(query)
    results = mb.get_artist(results[0]["id"])

    return render(request, "search.html", {"results": results})