import os


def GetTrackFiles(path: str) -> list[str]:
    """
    Get the track statistics from the JSON files
    """
    # Check if the directory exists
    if not os.path.exists(path):
        print(f"Directory {path} does not exist.")
        exit(1)

    # List all files in the directory
    files = os.listdir(path)
    streaming_history_files = [os.path.join(path, f) for f in files if f.startswith("Streaming_History_Audio_") and f.endswith(".json")]

    return streaming_history_files
