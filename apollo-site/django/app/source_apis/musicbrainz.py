import musicbrainzngs as mb
from . import ontology

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
    return mb.search_release(query=query)["release-list"]

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

def get_instruments(track_id):
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



"""
{'id': '66c662b6-6e2f-4930-8610-912e24c63ed1', 
'type': 'Group', 
'ext:score': '100', 
'name': 'AC/DC', 
'sort-name': 'AC/DC', 
'country': 'AU', 
'area': 
    {'id': '106e0bec-b638-3b37-b731-f53d507dc00e', 
    'type': 'Country', 
    'name': 'Australia', 
    'sort-name': 'Australia', 
    'life-span': 
        {'ended': 'false'}
    }, 
'begin-area': 
    {'id': '3f179da4-83c6-4a28-a627-e46b4a8ff1ed', 
    'type': 'City', 
    'name': 'Sydney', 
    'sort-name': 'Sydney', 
    'life-span': 
        {'ended': 'false'}
    }, 
'disambiguation': 'Australian hard rock band', 
'ipi-list': ['00133076008'], 
'isni-list': ['000000012271298X'], 
'life-span': 
    {'begin': '1973-11', 
    'ended': 'false'}, 
'alias-list': [
    {'sort-name': 'AC/DC', 
        'type': 'Artist name', 
        'begin-date': '1973-11', 
        'alias': 'AC/DC'}, 
    {'sort-name': 'AC|DC', 
        'type': 'Search hint', 
        'alias': 'AC|DC'}, 
    {'sort-name': 'Akka Dakka', 
        'type': 'Search hint', 
        'alias': 'Akka Dakka'}, 
    {'sort-name': 'Acca Dacca', 
        'type': 'Search hint', 
        'alias': 'Acca Dacca'}, 
    {'sort-name': 'AC.DC', 
        'type': 'Search hint', 
        'alias': 'AC.DC'}, 
    {'sort-name': 'AC⚡︎DC', 
        'type': 'Search hint', 
        'alias': 'AC⚡︎DC'}, 
    {'sort-name': 'ACDC', 
        'type': 'Search hint', 
        'alias': 'ACDC'}, 
    {'sort-name': 'AC-DC', 
        'type': 'Search hint', 
        'alias': 'AC-DC'}, 
    {'sort-name': 'AC⚡DC', 
        'type': 'Search hint', 
        'alias': 'AC⚡DC'}, 
    {'sort-name': 'AC?DC', '
        type': 'Search hint', 
        'alias': 'AC?DC'}, 
    {'sort-name': 'AC\\DC', 
        'type': 'Search hint', 
        'alias': 'AC\\DC'}, 
    {'sort-name': 'AC DC', 
        'type': 'Search hint', 
        'alias': 'AC DC'}
    ], 
'tag-list': [
    {'count': '13', 
        'name': 'rock'}, 
    {'count': '-1', 
        'name': 'heavy metal'}, 
    {'count': '-3', 
        'name': 'metal'}, 
    {'count': '0', 
        'name': 'australian'}, 
    {'count': '-1', 
        'name': 'band'}, 
    {'count': '45', 
        'name': 'hard rock'}, 
    {'count': '1', 
        'name': 'relaxed'}, 
    {'count': '9', 
        'name': 'blues rock'}, 
    ...
    ]}
"""
