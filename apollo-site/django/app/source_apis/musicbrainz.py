import musicbrainzngs as mb
import json

mb.set_useragent("apollo", "0.1", "http://localhost:8000")


# artists
def search_artist(query):
    return mb.search_artists(query=query)["artist-list"]

def get_artist(artist_id):
    return mb.get_artist_by_id(id=artist_id)["artist"]

def get_artist_albums(artist_id):
    return mb.browse_release_groups(artist=artist_id)["release-list"]

# albums
def search_album(query):
    return mb.search_releases(query=query)["release-list"]

def get_album(album_id):
    return mb.get_release_by_id(album_id)["release"]

def get_album_tracks(album_id):
    return mb.browse_recordings(release=album_id)["recording-list"]

def get_album_labels(album_id):
    return mb.browse_labels(release=album_id)["label-list"]

def get_album_artists(album_id):
    return mb.browse_artists(release=album_id)["artist-list"]

def get_album_cover_art(album_id):
    images = mb.get_image_list(release=album_id)["images"]
    for image in images:
        if image.get("front"):
            return image
    return None

def get_album_realese_type(album_id):
    release_type = mb.get_release_by_id(album_id)["release"]["release-group"]["type"]
    # map to album, broadcast, ep, single
    return release_type

# tracks
def search_track(query):
    return mb.search_recordings(recording=query)["recording-list"]

def get_track(track_id):
    return mb.get_recording_by_id(track_id)["recording"]


def get_track_albums(track_id):
    return mb.browse_release(recording=track_id)["release-list"]

def get_track_artists(track_id):
    return mb.browse_artists(recording=track_id)["artist-list"]

def get_track_cover_art(track_id):
    images = mb.get_image_list(recording=track_id)["images"]
    for image in images:
        if image.get("front"):
            return image
    return None
