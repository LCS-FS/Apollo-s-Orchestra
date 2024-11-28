Thing->CreativeWork
    ->  MusicPlaylist -> MusicAlbum
    ->  MusicPlaylist -> MusicRelease
    -> Organization -> PerformingGroup -> Music Group
    -> MusicRecording

Thing->Person


MusicAlbum
MusicGroup or Person
MusicRecording
MusicAlbumReleaseType ENUM(AlbumRelease, BroadcastRelease, EPRelease, SingleRelease)

"""
sugestão da prof: começar com o ([MusicGroup])(https://schema.org/MusicGroup) que é o mais genérico e depois ir para os mais específicos, à medida que for necessário

Se pensarmos nisto como uma arvore, o MusicGroup seria o nó raiz e os outros seriam os nós filhos
"""

```mermaid
graph LR
    MusicGroup[[MusicGroup]] --> album[[album]]
    MusicGroup --> genre([genre - **Text**])
    MusicGroup --> award[[award - **Text**]]
    MusicGroup --> DissolutionDate([DissolutionDate - **Date**])
    MusicGroup --> foundingLocation([foundingLocation - **Text**])
    MusicGroup --> foundingDate([foundingDate - **Date**])
    MusicGroup --> member[[member]]
    MusicGroup --> group_logo([logo - **URL**])
    MusicGroup --> group_about([description - **Text**])
    MusicGroup --> groupName([name - **Text**])

    member --> gender([gender - **Text**])
    member --> givenName([givenName - **Text**])
    member --> artistName([artistName - **Text**])
    member --> birthDate([birthDate - **Date**])
    member --> deathDate([deathDate - **Date**])
    member --> nationality([nationality - **Text**])
    member --> memberAbout([about - **Text**])

    album --> numTracks([numTracks - **Integer**])
    album --> track[[track]]
    album --> albumReleaseType[albumReleaseType - **ENUM**]
    album --> albumAbout([about - **Text**])
    album --> datePublished([datePublished - **Date**])
    album --> albumLogo([logo - **URL**])
    album --> albumName([name - **Text**])

    albumReleaseType --> AlbumRelease([AlbumRelease])
    albumReleaseType --> BroadcastRelease([BroadcastRelease])
    albumReleaseType --> EPRelease([EPRelease])
    albumReleaseType --> SingleRelease([SingleRelease])

    track --> duration([duration - **Duration**])
    track --> trackAbout([about - **Text**])
    track --> trackName([name - **Text**])
    track --> composer[[composer - **Text**]]
    track --> lyricist[[lyricist - **Text**]]
    track --> lyrics([lyrics - **Text**])
    track --> instrument[[instrument - **Text**]]
```