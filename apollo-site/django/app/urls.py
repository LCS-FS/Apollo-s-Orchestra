from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("artist/<str:artist_id>", views.artist, name="artist"),
    path("artistrdf/<str:artist_id>", views.artist_rdf, name="artist_rdf"),
    path("album/<str:album_id>", views.album, name="album"),
    path("albumrdf/<str:album_id>", views.album_rdf, name="album_rdf"),
    path("track/<str:track_id>", views.track, name="track"),
    path("trackrdf/<str:track_id>", views.track_rdf, name="track_rdf"),
]

