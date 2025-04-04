from dataclasses import dataclass


@dataclass
class ArtistStats:
    id: str
    name: str
    genres: list = None
    popularity: int = None
    followers: int = None
    image: str = ""


@dataclass
class TopTracks:
    main_artist: str
    id_artist: str
    feat_artists: list = None
    track_name: str = None
    album_name: str = None
    album_releasedate: int = None
    album_totaltracks: int = None
    track_duration: int = None
    track_popularity: int = None
    track_number: int = None
