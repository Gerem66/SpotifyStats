"""
Module for displaying CLI visualizations
"""
import json
from datetime import datetime
from typing import Dict, List
from src.track import Track


def print_header():
    """
    Print a header for the CLI visualization
    """
    print('╭──────────────────────────────────────────╮')
    print('│               SpotifyStats   \u001b[90mby @Gerem66\u001b[0m │')
    print('│   Analyze your Spotify listening data    │')
    print('╰──────────────────────────────────────────╯\n')

def extract_year_from_filename(filename: str) -> int:
    """
    Extract year from Spotify history filename
    Expected format: Streaming_History_Audio_YYYY-YYYY_n.json or Streaming_History_Audio_YYYY_n.json
    """
    # Get just the filename without the path
    base_name = filename.split('/')[-1]

    # Extract the part with the year
    parts = base_name.split('_')
    if len(parts) < 4:
        return datetime.now().year  # Default year if format is not recognized

    # The year part is before the file index, and after "Audio" or "Video"
    year_part = parts[3]

    # If year contains a file index (e.g.: 2022-2023_9.json)
    if '.' in year_part:
        # Remove .json extension
        year_part = year_part.split('.')[0]

    # If year contains an index (e.g.: 2022-2023_9)
    if '_' in year_part:
        year_part = year_part.split('_')[0]

    # If it's a year range (e.g.: 2019-2020)
    if '-' in year_part:
        # Take the first year of the range
        years = year_part.split('-')
        return int(years[0])
    else:
        # It's just a single year (e.g.: 2019)
        try:
            return int(year_part)
        except ValueError:
            return datetime.now().year  # Default year if conversion fails


def calculate_listening_time_by_year(tracks: List[Track]) -> Dict[int, float]:
    """
    Calculate total listening time by year in hours
    """
    listening_time_by_year = {}

    for track in tracks:
        # Extract year from listening date
        # Note: In Track object, we currently don't have access to the listening date
        # Assuming track.release_date exists or we have another method to determine it
        # For now, we assign each track to the current year as an example
        year = datetime.now().year if track.release_date is None else track.release_date.year

        # Convert ms to hours
        hours = track.duration_ms / (1000 * 60 * 60)

        if year not in listening_time_by_year:
            listening_time_by_year[year] = 0.0

        listening_time_by_year[year] += hours

    return listening_time_by_year


def calculate_listening_time_by_filename_year(filenames: List[str], tracks: List[Track]) -> Dict[int, float]:
    """
    Calculate total listening time by year based on filename years
    """
    # Map each track to the year extracted from the filename it comes from
    track_to_year = {}
    for filename in filenames:
        year = extract_year_from_filename(filename)
        # For each track from this file, associate the year
        # But since we don't have this information, we'll make an approximation
        for track in tracks:
            # This is a simplification; ideally, we would have an exact mapping
            track_to_year[track.id] = year

    # Calculate listening time by year
    listening_time_by_year = {}
    for track in tracks:
        # If we don't have the year for this track, skip
        if track.id not in track_to_year:
            continue

        year = track_to_year[track.id]
        hours = track.duration_ms / (1000 * 60 * 60)

        if year not in listening_time_by_year:
            listening_time_by_year[year] = 0.0

        listening_time_by_year[year] += hours

    return listening_time_by_year


def display_listening_time_bar_chart(listening_time_by_year: Dict[int, float], max_width: int = 50) -> None:
    """
    Display a bar chart of listening time by year

    Args:
        listening_time_by_year: Dictionary with years as keys and listening hours as values
        max_width: Maximum width of the chart in characters
    """
    print("=== Listening Time by Year ===", end="\n\n")

    if not listening_time_by_year:
        print("No listening data available.")
        return

    # Define column widths for consistent formatting
    year_width = 7   # Width of the "Year" column

    # Find the maximum value to scale the chart
    max_hours = max(listening_time_by_year.values())

    # Sort years
    sorted_years = sorted(listening_time_by_year.keys())

    # Formatted header
    header = f"{'Year'.ljust(year_width)}|  Chart"
    separator = "-" * year_width + "+" + "-" * (2 + max_width + 15)  # Extra width for value display

    print(header)
    print(separator)

    for year in sorted_years:
        hours = listening_time_by_year[year]

        # Calculate bar width proportional to listening time
        bar_width = int((hours / max_hours) * max_width) if max_hours > 0 else 0

        # Create the bar with █ characters
        bar = "█" * bar_width

        # Display the year and the bar with the value at the end
        print(f"{str(year).ljust(year_width)}|  {bar} {hours:.2f} hours")

    print(f"\nTotal listening time: {sum(listening_time_by_year.values()):.2f} hours")


def create_listening_year_graph_from_filenames(filenames: List[str]) -> None:
    """
    Create and display a graph of listening time by year based on filenames
    """
    # Create a dictionary of year -> tracks based on filenames
    tracks_by_year = {}
    total_duration_by_year = {}

    # Extract year from each filename
    for filename in filenames:
        base_filename = filename.split('/')[-1]  # Get just the filename without the path

        # Try to extract the year from the filename
        try:
            year = extract_year_from_filename(base_filename)

            # Initialize or retrieve the track list for this year
            if year not in tracks_by_year:
                tracks_by_year[year] = []
                total_duration_by_year[year] = 0.0

            # For each file, load and process its tracks
            with open(filename, 'r', encoding='utf-8') as f:
                # Here we simply count the number of tracks per file
                # in a real implementation, you would read the tracks from the file
                data = json.load(f)

                # Calculate total duration for this year
                for item in data:
                    # Convert ms to hours
                    if 'ms_played' in item:
                        total_duration_by_year[year] += item['ms_played'] / (1000 * 60 * 60)
        except (ValueError, IndexError):
            # If we can't extract the year, continue with the next file
            continue

    # Display the graph
    display_listening_time_bar_chart(total_duration_by_year)
