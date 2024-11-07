from django.shortcuts import render
from django.http import HttpResponse
import musicbrainzngs as mb

# Create your views here.
def index(request):
    return render(request, "index.html")

def search(request):
    query = request.GET.get("q")
    mb.set_useragent("apollo", "0.1", "http://localhost:8000")
    results = mb.search_artists(query)

    return render(request, "search.html", {"results": results})