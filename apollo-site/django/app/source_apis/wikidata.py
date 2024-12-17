from SPARQLWrapper import SPARQLWrapper, JSON
import json

def query_artist_details(artist_name):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(f"""
    SELECT ?artist ?artistLabel ?givenName ?pseudonym ?birthDate ?deathDate ?genderLabel ?nationalityLabel ?picture WHERE {{
      ?artist rdfs:label "{artist_name}"@en;  # Artist name
              wdt:P31 wd:Q5.                 # Instance of human
      OPTIONAL {{ ?artist wdt:P1477 ?givenName. }}         # Given name
      OPTIONAL {{ ?artist wdt:P742 ?pseudonym. }}       # Artist name
      OPTIONAL {{ ?artist wdt:P569 ?birthDate. }}         # Date of birth
      OPTIONAL {{ ?artist wdt:P570 ?deathDate. }}         # Date of death
      OPTIONAL {{ ?artist wdt:P21 ?gender. }}             # Gender
      OPTIONAL {{ ?artist wdt:P27 ?nationality. }}        # Nationality
      OPTIONAL {{ ?artist wdt:P18 ?picture. }}            # Picture URL
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    LIMIT 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def query_albums_by_artist(artist_name):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(f"""
    SELECT ?album ?albumLabel ?releaseDate WHERE {{
      ?artist rdfs:label "{artist_name}"@en; # Artist name
              wdt:P31 wd:Q5.                # Instance of human
      ?album wdt:P175 ?artist;              # Performer
             wdt:P31 wd:Q482994;            # Instance of album
             wdt:P577 ?releaseDate.         # Release date
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    LIMIT 20
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def query_tracks_by_album(album_name):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(f"""
    SELECT ?track ?trackLabel WHERE {{
      ?album rdfs:label "{album_name}"@en; # Album name
             wdt:P31 wd:Q482994.           # Instance of album
      ?track wdt:P361 ?album.              # Part of the album
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    LIMIT 20
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def query_track_details(track_name):
    """
    Queries Wikidata for details about a track by its name.

    Args:
        track_name (str): The name of the track to search for.

    Returns:
        dict: JSON-formatted response with track details.
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(f"""
    SELECT ?track ?trackLabel ?albumLabel ?artistLabel ?releaseDate WHERE {{
      ?track rdfs:label "{track_name}"@en; # Track name
             wdt:P31 wd:Q7302866.         # Instance of musical work
      OPTIONAL {{ ?track wdt:P361 ?album. }}       # Part of album
      OPTIONAL {{ ?track wdt:P175 ?artist. }}      # Performer/artist
      OPTIONAL {{ ?album wdt:P577 ?releaseDate. }} # Release date of album
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    LIMIT 10
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def query_band_members(band_name):
    """
    Queries Wikidata for the members of a band along with their details.

    Args:
        band_name (str): The name of the band to search for.

    Returns:
        dict: JSON-formatted response with band members and their details.
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(f"""
SELECT ?member ?memberLabel ?givenName ?artistName ?birthDate ?deathDate ?genderLabel ?nationalityLabel ?picture WHERE {{
  ?band rdfs:label "{band_name}"@en;          # Band name
        wdt:P31/wdt:P279* wd:Q215380.         # Instance of band or group
  {{
    ?band wdt:P527 ?member.                  # Members from band
  }} UNION {{
    ?member wdt:P361 ?band.                  # Band from member
  }}
  OPTIONAL {{ ?member wdt:P1477 ?birthName. }}         # Given name
  OPTIONAL {{ ?member wdt:P742 ?pseudonym. }}          # Artist name
  OPTIONAL {{ ?member wdt:P569 ?birthDate. }}          # Date of birth
  OPTIONAL {{ ?member wdt:P570 ?deathDate. }}          # Date of death
  OPTIONAL {{ ?member wdt:P21 ?gender. }}              # Gender
  OPTIONAL {{ ?member wdt:P27 ?nationality. }}         # Nationality
  OPTIONAL {{ ?member wdt:P18 ?picture. }}             # Picture URL
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}
LIMIT 20
""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def query_band_logo(band_name):
    """
    Queries Wikidata for the logo of a band.

    Args:
        band_name (str): The name of the band to search for.

    Returns:
        dict: JSON-formatted response with the band's logo URL.
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(f"""
    SELECT ?band ?logo WHERE {{
      ?band rdfs:label "{band_name}"@en;       # Band name
            wdt:P31/wdt:P279* wd:Q215380;      # Instance of band or group
            wdt:P154 ?logo.                   # Logo
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    LIMIT 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def query_band_dissolution_date(band_name):
    """
    Queries Wikidata for the dissolution date of a band.

    Args:
        band_name (str): The name of the band to search for.

    Returns:
        dict: JSON-formatted response with the band's dissolution date.
    """
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(f"""
    SELECT ?band ?dissolutionDate WHERE {{
      ?band rdfs:label "{band_name}"@en;       # Band name
            wdt:P31/wdt:P279* wd:Q215380;      # Instance of band or group
            wdt:P576 ?dissolutionDate.        # Dissolution date
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    LIMIT 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def query_album_record_by_MB_Id(MB_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    
    # SPARQL query to fetch album and logo based on MB ID
    query = f"""
    SELECT ?album ?albumLabel ?logo ?recordLabel WHERE {{
        ?album wdt:P436 "{MB_id}" .  # Match the album using MB ID (P436)
        OPTIONAL {{ ?album wdt:P264 ?recordLabel. }}  # Fetch the recordLabel (P264), if available
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    }}
    LIMIT 1
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    # Execute the query and return results
    results = sparql.query().convert()
    return results
