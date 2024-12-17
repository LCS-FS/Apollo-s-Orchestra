from typing import List, Optional
from enum import Enum
from datetime import date, timedelta
from rdflib import Graph, Namespace, Literal, RDF, URIRef
from rdflib.namespace import FOAF, DC, RDFS, XSD
from datetime import datetime

EX = Namespace("http://example.org/")

# Enum for AlbumReleaseType
class AlbumReleaseType(Enum):
    """
    Enum representing different types of album releases.

    Attributes:
        ALBUM (str): Represents a full album release.
        BROADCAST (str): Represents a broadcast release.
        EP (str): Represents an extended play (EP) release.
        SINGLE (str): Represents a single release.
    """
    ALBUM = "AlbumRelease"
    BROADCAST = "BroadcastRelease"
    EP = "EPRelease"
    SINGLE = "SingleRelease"
    OTHER = "OtherRelease"


# Member Class
class Member:
    """
    Represents a member with personal and biographical information.

    Attributes:
        gender (str): The gender of the member.
        given_name (str): The given name of the member.
        artist_name (str): The artist name of the member.
        birth_date (Optional[date]): The birth date of the member. Defaults to None.
        death_date (Optional[date]): The death date of the member. Defaults to None.
        nationality (Optional[str]): The nationality of the member. Defaults to None.
        about (Optional[str]): Additional information about the member. Defaults to None.
    """
    def to_rdf(self) -> Graph:
        g = Graph()
        member_uri = EX[f"member/{self.artist_name.replace(' ', '_')}"]
        g.add((member_uri, RDF.type, FOAF.Person))
        g.add((member_uri, FOAF.name, Literal(self.artist_name)))
        if self.given_name:
            g.add((member_uri, FOAF.givenName, Literal(self.given_name)))
        if self.gender:
            g.add((member_uri, FOAF.gender, Literal(self.gender)))
        if self.birth_date:
            g.add((member_uri, FOAF.birthday, Literal(self.birth_date.isoformat(), datatype=XSD.date)))
        if self.death_date:
            g.add((member_uri, EX.deathDate, Literal(self.death_date.isoformat(), datatype=XSD.date)))
        if self.nationality:
            g.add((member_uri, EX.nationality, Literal(self.nationality)))
        if self.picture:
            g.add((member_uri, FOAF.img, URIRef(self.picture)))
        return g

    def __init__(
        self,
        gender: str,
        given_name: str,
        artist_name: Optional[str] = None ,
        birth_date: Optional[date] = None,
        death_date: Optional[date] = None,
        nationality: Optional[str] = None,
        picture: Optional[str] = None,
    ):
        self.gender = gender
        self.given_name = given_name
        self.artist_name = artist_name
        self.birth_date = birth_date
        self.death_date = death_date
        self.nationality = nationality
        self.picture = picture
    
    def __repr__(self):
        return f"Member(\n\tgender={self.gender}, \n\tgiven_name={self.given_name}, \n\tartist_name={self.artist_name}, \n\tbirth_date={self.birth_date}, \n\tdeath_date={self.death_date}, \n\tnationality={self.nationality}, \n\tpicture={self.picture}\n)"


# Track Class
class Track:
    """
    A class to represent a musical track.

    Attributes:
        duration (Optional[timedelta]): The duration of the track.
        about (Optional[str]): A brief description or information about the track.
        name (str): The name of the track.
        composer (Optional[List[str]]): A list of composers of the track. Defaults to an empty list.
        lyricist (Optional[List[str]]): A list of lyricists of the track. Defaults to an empty list.
        lyrics (Optional[str]): The lyrics of the track.

    Methods:
        __init__: Initializes a Track instance with the provided attributes.
    """
    def to_rdf(self) -> Graph:
        g = Graph()
        track_uri = EX[f"track/{self.name.replace(' ', '_')}"]
        g.add((track_uri, RDF.type, EX.Track))
        g.add((track_uri, DC.title, Literal(self.name)))
        if self.duration:
            g.add(track_uri, EX.duration, Literal(self.duration), datatype=XSD.duration)
        if self.about:
            g.add((track_uri, DC.description, Literal(self.about)))
        if self.lyrics:
            g.add((track_uri, EX.lyrics, Literal(self.lyrics)))
        if self.logo:
            g.add((track_uri, FOAF.logo, URIRef(self.logo)))
        if self.id:
            g.add((track_uri, EX.id, Literal(self.id)))
        if self.music_group_name:
            g.add((track_uri, EX.musicGroupName, Literal(self.music_group_name)))
        if self.music_group_id:
            g.add((track_uri, EX.musicGroupId, Literal(self.music_group_id)))
        if self.album_name:
            g.add((track_uri, EX.albumName, Literal(self.album_name)))
        if self.album_id:
            g.add((track_uri, EX.albumId, Literal(self.album_id)))
        if self.score:
            g.add((track_uri, EX.score, Literal(self.score)))
        return g


    def __init__(
        self,
        id : str,
        name: str,
        duration: Optional[str],
        music_group_name: str,
        music_group_id: str,
        album_name: Optional[str],
        album_id: Optional[str],
        about: Optional[str] = None,
        lyrics: Optional[str] = None,
        logo: Optional[str] = None,
        score: Optional[int] = 0,
    ):
        self.id = id
        self.duration = duration
        self.about = about
        self.name = name
        self.lyrics = lyrics
        self.logo = logo
        self.music_group_name = music_group_name
        self.music_group_id = music_group_id
        self.album_name = album_name
        self.album_id = album_id
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score
    
    def __repr__(self):
        return f"Track(\n\tname={self.name}, \n\tduration={self.duration}, \n\tabout={self.about}, \n\tlyrics={self.lyrics}, \n\tmusic_group_name={self.music_group_name}, \n\tmusic_group_id={self.music_group_id}, \n\talbum_name={self.album_name}, \n\talbum_id={self.album_id}, \n\tlogo={self.logo}, \n\tscore={self.score}\n)"


# Album Class
class Album:
    """
    Represents a music album.

    Attributes:
        num_tracks (int): The number of tracks in the album.
        tracks (List[Track]): A list of tracks in the album.
        release_type (AlbumReleaseType): The type of release for the album (e.g., single, EP, album).
        about (Optional[str]): A description or additional information about the album.
        date_published (date): The date the album was published.
        name (str): The name of the album.
    """

    def to_rdf(self) -> Graph:
        g = Graph()
        album_uri = EX[f"album/{self.name.replace(' ', '_')}"]
        g.add((album_uri, RDF.type, EX.Album))
        g.add((album_uri, DC.title, Literal(self.name)))
        g.add((album_uri, EX.releaseType, Literal(self.release_type.value)))
        g.add((album_uri, DC.date, Literal(self.date_published.isoformat(), datatype=XSD.date)))
        if self.about:
            g.add((album_uri, DC.description, Literal(self.about)))
        if self.logo:
            g.add((album_uri, FOAF.logo, URIRef(self.logo)))
        if self.label in self.label:
            g.add((album_uri, EX.label, Literal(self.label)))
        for track in self.tracks:
            g += track.to_rdf()  # Add the track RDF data
            track_uri = EX[f"track/{track.name.replace(' ', '_')}"]
            g.add((album_uri, EX.hasTrack, track_uri))
        if self.score:
            g.add((album_uri, EX.score, Literal(self.score)))
        if self.artist_name:
            g.add((album_uri, EX.artistName, Literal(self.artist_name)))
        if self.artist_id:
            g.add((album_uri, EX.artistId, Literal(self.artist_id)))
        return g

    def __init__(
        self,
        id : str,
        num_tracks: int,
        tracks: List[Track],
        release_type: AlbumReleaseType,
        about: Optional[str],
        date_published: date,
        logo: Optional[str],
        name: str,
        label: Optional[str] = None,
        score: Optional[int] = 0,
        artist_name: Optional[str] = None,
        artist_id: Optional[str] = None,
    ):
        self.num_tracks = num_tracks
        self.tracks = tracks
        self.release_type = release_type
        self.about = about
        self.date_published = date_published
        self.logo = logo
        self.name = name
        self.label = label
        self.score = score
        self.artist_name = artist_name
        self.artist_id = artist_id
        self.id = id
    
    def __repr__(self):
        return f"Album(\n\tnum_tracks={self.num_tracks}, \n\ttracks={self.tracks}, \n\trelease_type={self.release_type}, \n\tabout={self.about}, \n\tdate_published={self.date_published}, \n\tname={self.name}, \n\tlabel={self.label}, \n\tscore={self.score}, \n\tartist_name={self.artist_name}, \n\tartist_id={self.artist_id}\n)"

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score


# MusicGroup Class
class MusicGroup:
    """
    A class to represent a music group.

    Attributes:
    ----------
    name : str
        The name of the music group.
    genre : Optional[str]
        The genre of the music group.
    awards : Optional[List[str]]
        A list of awards won by the music group.
    dissolution_date : Optional[date]
        The date when the music group was dissolved.
    founding_location : Optional[str]
        The location where the music group was founded.
    founding_date : date
        The date when the music group was founded.
    members : List[Member]
        A list of members in the music group.
    logo : Optional[str]
        The logo of the music group.
    description : Optional[str]
        A brief description of the music group.
    albums : Optional[List[Album]]
        A list of albums released by the music group.

    Methods:
    -------
    __init__(self, name: str, genre: Optional[str], awards: Optional[List[str]], 
             dissolution_date: Optional[date], founding_location: Optional[str], 
             founding_date: date, members: List[Member], logo: Optional[str], 
             description: Optional[str], albums: Optional[List[Album]] = None):
        Constructs all the necessary attributes for the music group object.
    """
    def to_rdf(self) -> Graph:
        g = Graph()
        group_uri = EX[f"musicgroup/{self.id}"]
        g.add((group_uri, RDF.type, FOAF.Group))
        g.add((group_uri, FOAF.name, Literal(self.name)))
        if self.genre:
            g.add((group_uri, EX.genre, Literal(self.genre)))
        for award in self.awards:
            g.add((group_uri, EX.award, Literal(award)))
        if self.dissolution_date:
            g.add((group_uri, EX.dissolutionDate, Literal(self.dissolution_date.isoformat(), datatype=XSD.date)))
        if self.founding_date:
            g.add((group_uri, EX.foundingDate, Literal(self.founding_date.isoformat(), datatype=XSD.date)))
        if self.founding_location:
            g.add((group_uri, EX.foundingLocation, Literal(self.founding_location)))
        if self.logo:
            g.add((group_uri, FOAF.logo, URIRef(self.logo)))
        if self.description:
            g.add((group_uri, DC.description, Literal(self.description)))
        for member in self.members:
            g += member.to_rdf()  # Add the member RDF data
            member_uri = EX[f"member/{member.artist_name.replace(' ', '_')}"]
            g.add((group_uri, FOAF.member, member_uri))
        for album in self.albums:
            g += album.to_rdf()  # Add the album RDF data
            album_uri = EX[f"album/{album.name.replace(' ', '_')}"]
            g.add((group_uri, EX.hasAlbum, album_uri))
        if self.score:
            g.add((group_uri, EX.score, Literal(self.score)))
        return g

    def __init__(
        self,
        id: str,
        name: str,
        genre: Optional[str],
        dissolution_date: Optional[date],
        founding_location: Optional[str],
        founding_date: date,
        members: List[Member],
        logo: Optional[str],
        description: Optional[str],
        score: Optional[int] = 0,
        awards: Optional[List[str]] = None,
        albums: Optional[List[Album]] = None,
    ):
        self.id = id
        self.name = name
        self.genre = genre
        self.awards = awards or []
        self.dissolution_date = dissolution_date
        self.founding_location = founding_location
        self.founding_date = founding_date
        self.members = members
        self.logo = logo
        self.description = description
        self.albums = albums or []
        self.score = score

    def __repr__(self):
        return f"MusicGroup(\n\tname={self.name}, \n\tgenre={self.genre},\n\tawards={self.awards} ,\n\tfounding_date={self.founding_date}, \n\tfounding_location={self.founding_location}, \n\tdissolution_date={self.dissolution_date},\n\tmembers={self.members}, \n\talbums={self.albums}, \n\tlogo={self.logo}, \n\tdescription={self.description}\n)"
    

    def __lt__(self, other):
        return self.score < other.score

    def __eq__(self, other):
        return self.score == other.score