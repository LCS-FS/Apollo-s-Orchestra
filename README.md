# Apollo's-Orchestra

![_ddf6a749-ac26-4439-9f77-1f2d3ddb87d7](https://github.com/user-attachments/assets/a06efd99-327f-4cc3-8da5-7b2b6a4ea683)


# Running

from the `apollo-site/django/` directory, run the following commands:

```bash
pipenv install django
pipenv run pipenv install
pipenv run python manage.py runserver
```

It will start the server at `http:///127.0.0.1::8000/`

# Ontology

We used the following ontology to represent the data:

*psa: a mermaid plugin for markdown is needed to be able to render the following graph*

```mermaid
graph LR
    MusicGroup[[MusicGroup]] --> album[[album]]
    MusicGroup --> genre([genre - **Text**])
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

    album --> numTracks([numTracks - **Integer**])
    album --> track[[track]]
    album --> albumAbout([about - **Text**])
    album --> datePublished([datePublished - **Date**])
    album --> albumLogo([logo - **URL**])
    album --> albumName([name - **Text**])

    track --> trackName([name - **Text**])
    track --> lyrics([lyrics - **Text**])
```
