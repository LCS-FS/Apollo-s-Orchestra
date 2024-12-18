from .source_apis import lastfm, lyrics as lyricslib, musicbrainz, wikidata, ontology
import json
from rdflib import Graph
from datetime import datetime
import re

def get_artist_aux(artist):
    try:
        band_members = []
        artist_lastfm = lastfm.search_artist_by_mbid(artist['id'])

        name = artist["name"]
        genre = artist['disambiguation']
        try:
            foundind_date = datetime.strptime(artist['life-span']['begin'].split('T')[0], '%Y-%m-%d').date() if 'begin' in artist['life-span'] else None
        except:
            foundind_date = None
        founding_location = f"{artist['begin-area']['name']}, {artist['area']['name']}" if 'begin-area' in artist and 'area' in artist else None
        description = artist_lastfm.get_bio_content()
        id = artist['id']

        if artist['type'] == 'Group':
            try:
                dissolution_date = datetime.strptime(artist['life-span']['end'].split('T')[0], '%Y-%m-%d').date() if 'end' in artist['life-span'] else None
            except:
                dissolution_date = None
            logo = wikidata.query_band_logo(name)['results']['bindings'][0]['logo']['value']
        
            members = wikidata.query_band_members(name)['results']['bindings']
            members = [member['memberLabel']['value'] for member in members]

            for member_s in members:
                member = wikidata.query_artist_details(member_s)
                try:
                    member = member['results']['bindings'][0]
                    band_members.append(ontology.Member(
                        given_name=member['givenName']['value'] if 'givenName' in member else member['pseudonym']['value'] if 'pseudonym' in member else member['artistLabel']['value'],
                        gender=member['genderLabel']['value'],
                        artist_name=member['pseudonym']['value'] if 'pseudonym' in member else member['artistLabel']['value'] if 'artistLabel' in member else member['givenName']['value'] ,
                        birth_date=datetime.strptime(member['birthDate']['value'].split('T')[0], '%Y-%m-%d').date() if 'birthDate' in member else None,
                        death_date=datetime.strptime(member['deathDate']['value'].split('T')[0], '%Y-%m-%d').date() if 'deathDate' in member else None,
                        nationality=member['nationalityLabel']['value'] if 'nationalityLabel' in member else None,
                        picture=member['picture']['value'] if 'picture' in member else None
                    ))
                except Exception as e:
                    print(f"\033[91m{e}\033[0m")
                    pass
        elif artist['type'] == 'Person':
            try:
                dissolution_date = artist['life-span']['end'] if 'end' in artist['life-span'] else None
            except:
                dissolution_date = None
            member = wikidata.query_artist_details(name)['results']['bindings'][0]
            logo = member['picture']['value'] if 'picture' in member else None

            band_members.append(ontology.Member(
                given_name=member['givenName']['value'] if 'givenName' in member else member['pseudonym']['value'] if 'pseudonym' in member else None,
                gender=member['genderLabel']['value'],
                artist_name=member['pseudonym']['value'] if 'pseudonymLabel' in member else None,
                birth_date=member['birthDate']['value'].split('T')[0],
                death_date=member['deathDate']['value'].split('T')[0] if 'deathDate' in member else None,
                nationality=member['nationalityLabel']['value'] if 'nationalityLabel' in member else None,
                picture=member['picture']['value'] if 'picture' in member else None
            ))
        else :
            return None
        
        band_members = list({member.artist_name: member for member in band_members}.values())

        artist_obj = ontology.MusicGroup(
            name=name,
            genre=genre,
            id=id,
            founding_date=foundind_date,
            founding_location=founding_location,
            description=description,
            dissolution_date=dissolution_date,
            logo=logo,
            members=band_members
        )
        try:
            # Convert artist_obj to an RDF graph
            g = artist_obj.to_rdf()

            # Print the graph in Turtle format
            print("Serialized RDF Graph in Turtle format:")
            print(g.serialize(format="turtle"))
        except Exception as e:
            print(f"Error while serializing RDF graph: {e}")
        return artist_obj
    except Exception as e:
        print(f"\033[91m{e}\033[0m")
        return None

def get_track_aux(track, album_id=None, album_name=None, image_url=None, artist_id = None, artist_name = None):
    track_lastfm = lastfm.search_track_by_mbid(track['id'])
    print(track)
    
    logo = None

    if not (artist_id and artist_name):
        try:
            artist = musicbrainz.get_track_artists(track['id'])
            artist_name = artist[0]['name']
            artist_id = artist[0]['id']
        except:
            artist_name = None
            artist_id = None
    
    if not album_id:
        try:
            album = musicbrainz.get_track_albums(track['id'])
            album_name = album[0]['title']
            album_id = album[0]['id']
        except:
            album_name = None
            album_id = None

    if not image_url:
        try:
            logo = lastfm.get_album_cover(album_id)
        except:
            try:
                logo = lastfm.get_album_cover(track['release-list'][0]['id'])
            except: 
                logo = None
    else:
        logo = image_url


    print(f"Artist: {artist_name} {track['title']}")
    try:
        lyrics = lyricslib.get_lyrics(artist_name, track['title'])
        print(lyrics)
    except:
        try:
            lyrics = lyricslib.get_lyrics(track['artist-credit'][0]['artist']['name'], track['title'])
        except:
            lyrics = None

    track_obj = ontology.Track(
        name=track['title'],
        score=track['ext:score'] if 'ext:score' in track else None,
        id=track['id'],
        duration=f"{int(track['length']) // 60000}:{int(track['length']) % 60000}",
        music_group_id=track['artist-credit'][0]['artist']['id'] if 'artist-credit' in track else artist_id,
        music_group_name=track['artist-credit'][0]['artist']['name'] if 'artist-credit' in track else artist_name,
        album_id=track['release-list'][0]['id'] if 'release-list' in track else album_id,
        album_name=track['release-list'][0]['title'] if 'release-list' in track else album_name,
        about=track_lastfm.get_wiki_content(),
        logo=logo,
        lyrics=lyrics
    )
    try:
        # Convert artist_obj to an RDF graph
        g = track_obj.to_rdf()

        # Print the graph in Turtle format
        print("Serialized RDF Graph in Turtle format:")
        print(g.serialize(format="turtle"))
    except Exception as e:
        print(f"Error while serializing RDF graph: {e}")
    print("track success")
    return track_obj

def parse_date(album):
    date_str = None
    
    if 'date' in album:
        date_str = album['date']
    elif 'first-release-date' in album:
        date_str = album['first-release-date']
    
    if date_str:
        # Regular expression to match 'YYYY', 'YYYY-MM', 'YYYY-MM-DD' formats
        match = re.match(r'(\d{4})(?:-(\d{1,2})(?:-(\d{1,2}))?)?', date_str)
        if match:
            year = int(match.group(1))
            month = int(match.group(2)) if match.group(2) else 1
            day = int(match.group(3)) if match.group(3) else 1
            
            try:
                return datetime(year, month, day).date()
            except ValueError:
                return None
    
    return None

def get_album_aux(album, artist_id=None, artist_name=None):
    #wikidata: label, logo, 
    wikidata_album = wikidata.query_album_record_by_MB_Id(album['id'])
    
    label = wikidata_album['results']['bindings']['recordLabel']['value'] if 'recordLabel' in wikidata_album['results']['bindings'] else None
    

    try:
        artist = musicbrainz.get_album_artists(album['id'])
        artist_name = artist[0]['name']
        artist_id = artist[0]['id']
    except:
        artist_name = None
        artist_id = None

    print(f"Artist: {artist_name} ({artist_id})")

    album_obj = ontology.Album(
        name=album['title'],
        id=album['id'],
        artist_name=artist_name if artist_name else album['artist-credit'][0]['artist']['name'] if 'artist-credit' in album else artist_name,
        artist_id=artist_id if artist_id else album['artist-credit'][0]['artist']['id'] if 'artist-credit' in album else artist_id,
        about = None,
        release_type=album['release-group']['type'] if 'release-group' in album else album['primary-type'] if 'primary-type' in album else None,
        #date_published=datetime.strptime(album['date'], '%Y').date() if 'date' in album else datetime.strptime(album['first-release-date'], '%Y').date() if 'first-release-date' in album else None,
        date_published=parse_date(album),
        num_tracks=album['medium-track-count'] if 'medium-track-count' in album else None,
        tracks=None,
        label=label,
        score=album['ext:score'] if 'ext:score' in album else None,
        logo=lastfm.get_album_cover(album['id'])
    )
    print(album_obj.logo)
    try:
        # Convert artist_obj to an RDF graph
        g = album_obj.to_rdf()

        # Print the graph in Turtle format
        print("Serialized RDF Graph in Turtle format:")
        print(g.serialize(format="turtle"))
    except Exception as e:
        print(f"Error while serializing RDF graph: {e}")

    print("Fuck")
    return album_obj

def fetch_artist(query):
    artist_obj_list = []
    artist_mb = musicbrainz.search_artist(query)
    # from str to json
    for artist in artist_mb:
        artist_obj = get_artist_aux(artist)
        if artist_obj:
            artist_obj_list.append(artist_obj)
    return artist_obj_list

def fetch_artist_from_id(artist_id):
    artist = musicbrainz.get_artist(artist_id)
    return get_artist_aux(artist)

def fetch_album(query):
    albums_obj_list = []
    albums_mb = musicbrainz.search_album(query)

    for album in albums_mb:
        try:
            album_obj = get_album_aux(album)
            albums_obj_list.append(album_obj)
        except Exception as e:
            print(f"\033[91m{e}\033[0m")
    return albums_obj_list

def fetch_album_from_id(album_id):
    album = musicbrainz.get_album(album_id)
    return get_album_aux(album)

def fetch_track(query):
    tracks = musicbrainz.search_track(query)
    tracks_obj_list = []

    for track in tracks:
        try:
            track_obj = get_track_aux(track)
            tracks_obj_list.append(track_obj)
        except Exception as e:
            print(f"\033[91m{e}\033[0m")
    return tracks_obj_list

def fetch_track_from_id(track_id):
    track = musicbrainz.get_track(track_id)
    print(track)
    albums = musicbrainz.get_track_albums(track_id)
    artists = musicbrainz.get_track_artists(track_id)
    print(f"Artist: {artists}")
    album_name = albums[0]['title']
    artist_name = artists[0]['name']
    album_id = albums[0]['id']
    artist_id = artists[0]['id']
    return get_track_aux(track, album_id=album_id, album_name=album_name, artist_id=artist_id, artist_name=artist_name)

def join_artist_albums(artist_obj):
    albums = musicbrainz.get_artist_albums(artist_obj.id)
    print("DICK SIZE: " , len(albums))
    albums_obj_list = []
    for album in albums:
        try:
            album_obj = get_album_aux(album, artist_id = artist_obj.id, artist_name=artist_obj.name)
            albums_obj_list.append(album_obj)
        except Exception as e:
            print(f"\033[91m{e}\033[0m")
    
    artist_obj.albums = albums_obj_list
    return artist_obj

def join_album_tracks(album_obj):
    tracks = musicbrainz.get_album_tracks(album_obj.id)
    tracks_obj_list = []
    for track in tracks:
        try:
            track_obj = get_track_aux(track, album_id=album_obj.id, album_name=album_obj.name, image_url=album_obj.logo, artist_id=album_obj.artist_id, artist_name=album_obj.artist_name)
            tracks_obj_list.append(track_obj)
        except Exception as e:
            print(f"\033[91m{e}\033[0m")
    
    album_obj.tracks = tracks_obj_list
    album_obj.num_tracks = len(tracks_obj_list)
    return album_obj