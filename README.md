# Metronome Application

This is a graphical Metronome application that integrates with Spotify to fetch and display the BPM (beats per minute) and key of the currently playing track. The application is built using `tkinter` for the GUI, `spotipy` for Spotify integration, and `pygame` for metronome functionality.

## Features

- Displays the BPM and key of the currently playing Spotify track.
- Provides manual BPM adjustment.
- Allows toggling of the metronome sound.
- OAuth authentication with Spotify.
- Fetches and displays the currently playing track's name and artist.

## Requirements

- Python 3.x
- `tkinter` (usually comes with Python standard library)
- `spotipy` (Spotify Web API wrapper)
- `pygame` (for metronome sound)
- Spotify Developer credentials (Client ID, Client Secret, Redirect URI)

## Installation

1. Clone the repository:

```sh
git clone <repository-url>
cd <repository-directory>

2. Install the required packages:

pip install spotipy pygame


3. Set up your Spotify Developer credentials to enter into the python script.

Usage

1. Run the script:
    python metro.py
        
2. If the Spotify API credentials are not set, a window will prompt you to enter them manually.
    
3. The main application window will open. If a Spotify track is playing, it will display the track’s BPM and key. Stop Metronome by Pausing on Spotify
