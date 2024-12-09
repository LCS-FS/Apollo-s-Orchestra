from source_apis import lastfm, lyrics, musicbrainz, wikidata, ontology

def fetch_artist(query):
    artist_mb = musicbrainz.search_artist(query)
    for artist in artist_mb:
        artist_lastfm = lastfm.search_artist_by_mbid(artist['id'])

        name = artist["name"]
        genre = artist['disambiguation']
        foundind_date = artist['life-span']['begin']
        founding_location = f"{artist['begin-area']['name']}, {artist['area']['name']}"
        description = artist_lastfm.get_bio_content()
        if artist['life-span']['ended']:
            # go get from wikidata
            dissolution_date = wikidata.query_band_dissolution_date(name)['results']['bindings'][0]['dissolutionDate']['value'].split('T')[0]
        logo = wikidata.query_band_logo(name)['results']['bindings'][0]['logo']['value']

        if artist['type'] == 'Group':
            members = wikidata.query_band_members(name)['results']['bindings']
            members = [member['memberLabel']['value'] for member in members]

            for member in members:
                
        else:
        

def fetch_artist_rdf(artist_name):
    return None

def fetch_album(query):
    return None

def fetch_album_rdf(album_name):
    return None

def fetch_track(query):
    return None

def fetch_track_rdf(track_name):
    return None