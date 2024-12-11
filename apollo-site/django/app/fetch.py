from source_apis import lastfm, lyrics, musicbrainz, wikidata, ontology
import json

def fetch_artist(query):
    artist_obj_list = []
    artist_mb = musicbrainz.search_artist(query)
    # from str to json
    for artist in artist_mb:
        try:
            band_members = []
            artist_lastfm = lastfm.search_artist_by_mbid(artist['id'])

            name = artist["name"]
            genre = artist['disambiguation']
            foundind_date = artist['life-span']['begin']
            founding_location = f"{artist['begin-area']['name']}, {artist['area']['name']}"
            description = artist_lastfm.get_bio_content()
            if artist['life-span']['ended']:
                dissolution_date = wikidata.query_band_dissolution_date(name)['results']['bindings'][0]['dissolutionDate']['value'].split('T')[0]
            logo = wikidata.query_band_logo(name)['results']['bindings'][0]['logo']['value']

            if artist['type'] == 'Group':
                members = wikidata.query_band_members(name)['results']['bindings']
                members = [member['memberLabel']['value'] for member in members]

                for member_s in members:
                    member = wikidata.query_artist_details(member_s)
                    print(member)
                    print(type(member))
                    print("#####################")
                    try:
                        member = member['results']['bindings'][0]
                        band_members.append(ontology.Member(
                            given_name=member['givenName']['value'] if 'givenName' in member else member['pseudonym']['value'] if 'pseudonym' in member else None,
                            gender=member['genderLabel']['value'],
                            artist_name=member['pseudonym']['value'] if 'pseudonymLabel' in member else None,
                            birth_date=member['birthDate']['value'].split('T')[0],
                            death_date=member['deathDate']['value'].split('T')[0] if 'deathDate' in member else None,
                            nationality=member['nationalityLabel']['value'] if 'nationalityLabel' in member else None,
                            picture=member['picture']['value'] if 'picture' in member else None
                        ))
                    except:
                        pass
            elif artist['type'] == 'Person':
                member = wikidata.query_artist_details(name)['results']['bindings'][0]
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
                continue
            artist_obj_list.append(ontology.MusicGroup(
                name=name,
                genre=genre,

                founding_date=foundind_date,
                founding_location=founding_location,
                description=description,
                dissolution_date=dissolution_date,
                logo=logo,
                members=band_members
            ))
            print("success")
        except Exception as e:
            print(f"\033[91m{e}\033[0m")
            continue
    return artist_obj_list


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

if __name__ == '__main__':
    #TODO: Fix issue with single artists search
    results = fetch_artist('Elton John')
    print(len(results))
    for result in results:
        print(result)
        print("##############################")
