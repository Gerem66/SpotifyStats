# SpotifyStats

A Python tool to analyze your Spotify listening history and extract statistics about your music habits.

## Overview

SpotifyStats processes your Spotify streaming history data to provide insights like:
- Most played tracks
- Favorite artists
- Listening time by album
- Visualization of listening time by year
- And more...

## Prerequisites

- Python 3.10 or newer
- Your Spotify streaming history data (JSON files)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Gerem66/SpotifyStats.git
cd SpotifyStats
```

2. No additional dependencies are required as the project uses only Python standard libraries.

## Getting Your Spotify Data

1. **Request your Spotify data**:
   - Go to your [Spotify Account Privacy Settings](https://www.spotify.com/account/privacy/)
   - Scroll down to "Download your data" section
   - Click "Request data"
   - Spotify will prepare your data and notify you by email when it's ready (can take up to 30 days)

2. **Download and extract your data**:
   - Once you receive the email from Spotify, download the ZIP file(s)
   - Extract the ZIP file(s)
   - Look for files named `Streaming_History_Audio_*.json` in the extracted folder

3. **Move data files to the project**:
   - Place all `Streaming_History_Audio_*.json` files in the `data/` directory of this project
   - You can also include `Streaming_History_Video_*.json` files if you want to analyze your video streaming history

## Usage

Run the main script:

```bash
python main.py
```

By default, the script will look for streaming history JSON files in the `data/` directory. If your data files are in a different location, you can modify the file paths in `main.py`.

## Customization

You can customize which statistics to display by modifying the `main.py` file:

- Change sorting criteria between "duration" and "play_count"
- Filter by artist, album, or track title
- Adjust the number of results to display

## Example Results

### Top Tracks by Duration
```
Top Tracks:
1.   Bohemian Rhapsody - Queen                                   12.75 hours
2.   Stairway to Heaven - Led Zeppelin                            9.32 hours
3.   Hotel California - Eagles                                    8.47 hours
4.   Imagine - John Lennon                                        7.85 hours
5.   Thriller - Michael Jackson                                   6.19 hours
```

### Listening Time by Year Visualization
```
=== Listening Time by Year ===

Year   |  Chart
-------+-----------------------------------------------------------------
2017   |  ████████████ 125.45 hours
2018   |  ███████████████████████████ 287.32 hours
2019   |  ████████████████████████████████ 345.67 hours
2020   |  ████████████████████████████████████████ 412.89 hours
2021   |  ███████████████████████████████████ 378.56 hours
2022   |  ████████████████████████████ 301.44 hours
2023   |  ████████████████████████████████████████ 412.75 hours
2024   |  ███████████████████████████ 289.15 hours

Total listening time: 2553.23 hours
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
