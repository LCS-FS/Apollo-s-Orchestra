from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("artist/<str:artist_id>", views.artist, name="artist"),
    path("api/artist/<str:artist_id>", views.artist_api, name="artist_api"),
    path("album/<str:album_id>", views.album, name="album"),
    path("api/album/<str:album_id>", views.album_api, name="album_api"),
    path("track/<str:track_id>", views.track, name="track"),
    path("api/track/<str:track_id>", views.track_api, name="track_api"),
]

