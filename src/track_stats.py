import json
from typing import Literal
from src.track import Track


SORT_FROM: Literal["all", "artist", "title", "album"] = "artist"
SORT_BY: Literal["duration", "play_count"] = "duration"


class TrackStats:
    """
    Class to store a track statistics
    """
    def __init__(self, all_tracks: list[Track] = []):
        self.all_tracks = all_tracks

    def LoadTracksFromFiles(self, files: list[str]):
        """
        Load tracks from JSON files
        """
        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    self.all_tracks.append(Track.from_json(item))

    def GetByID(self, track_id: str) -> Track:
        """
        Return the track corresponding to the given ID
        """
        for track in self.all_tracks:
            if track.id == track_id:
                return track
        raise ValueError(f"Track with ID {track_id} not found")

    def GetTopTracks(
            self,
            from_filter: Literal["all", "artist", "title", "album"],
            filter_value: str = "",
            sort_by: Literal["duration", "play_count"] = "duration",
            top_n: int = 10
        ) -> dict[Track, float]:
        """
        Return the best avenues according to the specified criteria

        Args:
            from_filter: The filter to apply ("all", "artist", "title", "album")
            filter_value: The value of the filter (artist name, title or album, empty string for "all")
            sort_by: The sorting criterion ("duration" or "play_count")
            top_n: Number of tracks to return

        Returns:
            A dictionary with tracks as keys and values (duration or number of readings) as values
        """
        filtered_tracks: list[Track] = []

        # Track filtering according to the requested criterion
        if from_filter == "all":
            filtered_tracks = self.all_tracks
        elif from_filter == "artist":
            filtered_tracks = [track for track in self.all_tracks if filter_value in track.artists]
        elif from_filter == "title":
            filtered_tracks = [track for track in self.all_tracks if filter_value.lower() in (track.name or '').lower()]
        elif from_filter == "album":
            filtered_tracks = [track for track in self.all_tracks if filter_value.lower() in (track.album_name or '').lower()]

        # Creation of a dictionary to bring together the tracks with the same title, artist and album
        track_groups: dict[tuple[str, str, str], list[Track]] = {}
        for track in filtered_tracks:
            key = (track.name or '', ','.join(sorted(track.artists)), track.album_name or '')
            if key not in track_groups:
                track_groups[key] = []
            track_groups[key].append(track)

        # Calculation of values ​​according to the sorting criterion for each group of tracks
        track_values: dict[Track, float] = {}

        for key, tracks in track_groups.items():
            # Take the first track as representative of the group
            representative_track = tracks[0]

            value = 0.0
            for track in tracks:
                if sort_by == "duration":
                    value += track.duration_ms / (1000 * 60)  # Minute
                elif sort_by == "play_count":
                    value += 1

            track_values[representative_track] = value

        # Sorting
        sorted_tracks = sorted(track_values.items(), key=lambda x: x[1], reverse=True)

        # Limitation to the number requested
        top_tracks = {}
        for i in range(min(top_n, len(sorted_tracks))):
            track, value = sorted_tracks[i]
            top_tracks[track] = value

        return top_tracks

    def PrintTopTracks(self, from_filter: Literal["all", "artist", "title", "album"], filter_value: str = "", sort_by: Literal["duration", "play_count"] = "duration", top_n: int = 10) -> None:
        """
        Displays the best tracks according to the specified criteria

        Args:
            from_filter: The filter to apply ("all", "artist", "title", "album")
            filter_value: The value of the filter (artist name, title or album)
            sort_by: The sorting criterion ("duration" or "play_count")
            top_n: Number of tracks to return
        """
        top_tracks = self.GetTopTracks(from_filter, filter_value, sort_by, top_n)

        # Build an appropriate title for display
        title = "Top Tracks"
        if from_filter != "all":
            if from_filter == "artist":
                title += f" par {filter_value}"
            elif from_filter == "title":
                title += f" avec le titre contenant '{filter_value}'"
            elif from_filter == "album":
                title += f" de l'album '{filter_value}'"

        print(f"=== {title} ===", end="\n\n")

        if len(top_tracks) == 0:
            print(f"No tracks found.")

        for i in range(len(top_tracks)):
            track, value = list(top_tracks.items())[i]
            if sort_by == "duration":
                # Convert the minutes to the display for the display
                print(f"{(str(i + 1) + '.').ljust(4)} {str(track).ljust(60)} {value / 60:.2f} hours")
            else:  # sort_by == "play_count"
                print(f"{(str(i + 1) + '.').ljust(4)} {str(track).ljust(60)} {int(value)} plays")

        print()
