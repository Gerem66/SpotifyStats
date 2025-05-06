import os
from src.utils import GetTrackFiles
from src.track_stats import TrackStats
from src.cli_visualization import print_header, create_listening_year_graph_from_filenames


def main():
    """
    Main function to run the CLI visualization
    """

    path = os.getcwd() + "/data"


    # Get the track statistics
    trackFiles = GetTrackFiles(path)
    trackStats = TrackStats()
    trackStats.LoadTracksFromFiles(trackFiles)

    # Print the top tracks by duration
    trackStats.PrintTopTracks('all', sort_by='duration', top_n=10)

    # Example usage of PrintTopTracks
    # trackStats.PrintTopTracks('artist', 'Orelsan', sort_by='duration', top_n=10)
    # trackStats.PrintTopTracks('artist', 'KIK', sort_by='play_count', top_n=10)
    # trackStats.PrintTopTracks('artist', 'Vald')
    # trackStats.PrintTopTracks('album', 'Agartha')
    # trackStats.PrintTopTracks('title', 'SPQR')

    # Basic statistics
    print("=== Basic Statistics ===\n")
    print("Total tracks listened:", len(trackStats.all_tracks))
    print("Unique tracks listened:", len(set(track.id for track in trackStats.all_tracks)))
    print(f"Total Duration of All Tracks: {sum(track.duration_ms for track in trackStats.all_tracks) / (1000 * 60 * 60):.2f} hours", end="\n\n")

    # Show the graphic for listening time per year
    create_listening_year_graph_from_filenames(trackFiles)

if __name__ == "__main__":
    print_header()
    main()
