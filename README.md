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


3. Set up your Spotify Developer credentials as environment variables:
export SPOTIPY_CLIENT_ID='your-client-id'
export SPOTIPY_CLIENT_SECRET='your-client-secret'
export SPOTIPY_REDIRECT_URI='your-redirect-uri'

Usage

1. Run the script:
    python metro.py
        
2. If the Spotify API credentials are not set, a window will prompt you to enter them manually.
    
3. The main application window will open. If a Spotify track is playing, it will display the track’s BPM and key. You can start and stop the metronome using the provided controls.

Code Overview
The script is structured as follows:

    •    MetronomeApp class: Main application class
    •    __init__: Initializes the main application window and sets up the Spotify OAuth.
    •    wipe_cached_token: Removes the cached Spotify token.
    •    init_app: Initializes the Spotify OAuth object and checks for a cached token.
    •    credentials_window: Prompts the user to enter Spotify API credentials.
    •    create_widgets: Creates and arranges the application widgets (buttons, labels, etc.).
    •    start_metronome: Starts the metronome in a separate thread.
    •    stop_metronome: Stops the metronome.
    •    play_metronome: Plays the metronome sound at the specified BPM.
    •    toggle_track_id: Toggles the visibility of the track ID entry.
    •    authenticate_spotify: Handles the Spotify authentication process.
    •    fetch_currently_playing_track: Fetches the currently playing Spotify track and updates the UI.
    •    get_track_audio_features: Retrieves the audio features (BPM and key) of the given track.
    •    update_bpm_and_key: Updates the BPM and key display.
    •    update_track_name: Updates the track name display.
    •    on_closing: Handles application cleanup on closing.
