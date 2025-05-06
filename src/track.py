from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Track:
    """Représentation d'une piste (track) Spotify"""

    id: str
    name: str
    artists: list[str]
    album_name: str
    album_id: str
    duration_ms: int
    explicit: bool
    popularity: int
    preview_url: Optional[str] = None
    external_url: Optional[str] = None
    release_date: Optional[datetime] = None

    # Audio characteristics
    danceability: Optional[float] = None
    energy: Optional[float] = None
    key: Optional[int] = None
    loudness: Optional[float] = None
    mode: Optional[int] = None
    speechiness: Optional[float] = None
    acousticness: Optional[float] = None
    instrumentalness: Optional[float] = None
    liveness: Optional[float] = None
    valence: Optional[float] = None
    tempo: Optional[float] = None

    @classmethod
    def from_json(cls, json_data: dict[str, any]) -> 'Track':
        """
        Creates a track instance from a JSON dictionary

        The expected format corresponds to the response of the Spotify API for a track,
        possibly enriched with the audio characteristics
        """
        # Extraction of the track ID from Uri Spotify
        track_uri = json_data.get('spotify_track_uri', '')
        track_id = track_uri.split(':')[-1] if track_uri else ''

        # Extraction of basic metadata
        track_name = json_data.get('master_metadata_track_name', '')
        artist_name = json_data.get('master_metadata_album_artist_name', '')
        artists = [artist_name] if artist_name else []
        album_name = json_data.get('master_metadata_album_album_name', '')
        album_id = ''
        duration_ms = json_data.get('ms_played', 0)
        explicit = False
        popularity = 0

        return cls(
            id=track_id,
            name=track_name,
            artists=artists,
            album_name=album_name,
            album_id=album_id,
            duration_ms=duration_ms,
            explicit=explicit,
            popularity=popularity,
            preview_url=json_data.get('preview_url'),
            external_url=json_data.get('external_url'),
            release_date=None,
            danceability=json_data.get('danceability'),
            energy=json_data.get('energy'),
            key=json_data.get('key'),
            loudness=json_data.get('loudness'),
            mode=json_data.get('mode'),
            speechiness=json_data.get('speechiness'),
            acousticness=json_data.get('acousticness'),
            instrumentalness=json_data.get('instrumentalness'),
            liveness=json_data.get('liveness'),
            valence=json_data.get('valence'),
            tempo=json_data.get('tempo')
        )

    @property
    def duration_minutes(self) -> float:
        """Return the duration in minutes"""
        return self.duration_ms / 60000

    @property
    def artist_names(self) -> str:
        """Return the names of artists separated by commas"""
        return ", ".join(self.artists)

    def __str__(self) -> str:
        return f"{self.name} - {self.artist_names}"

    def __hash__(self):
        """Allows you to use track as a key in a dictionary"""
        return hash(self.id)
