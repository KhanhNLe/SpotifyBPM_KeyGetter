import tkinter as tk
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pygame
import time
import threading

# Replace these with your own Spotify API credentials
client_id = 'Put Your Own'
client_secret = 'Put Your Own'
redirect_uri = 'http://localhost:8888/callback'

# Set up the Spotify OAuth object
sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope="user-read-playback-state user-library-read")

class MetronomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Metronome")
        
        # Initialize pygame mixer
        pygame.mixer.init()
        self.tick_sound = pygame.mixer.Sound("tick.wav")  # Ensure you have a tick.wav file in the same directory

        self.bpm = 60
        self.key = None
        self.is_running = False

        self.create_widgets()
    
    def create_widgets(self):
        self.bpm_label = ttk.Label(self.root, text="BPM:")
        self.bpm_label.pack(pady=10)

        self.bpm_entry = ttk.Entry(self.root, width=10)
        self.bpm_entry.pack(pady=10)
        self.bpm_entry.insert(0, "60")

        self.start_button = ttk.Button(self.root, text="Start", command=self.start_metronome)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_metronome)
        self.stop_button.pack(pady=10)

        self.track_entry = ttk.Entry(self.root, width=30)
        self.track_entry.pack(pady=10)

        self.fetch_bpm_button = ttk.Button(self.root, text="Fetch BPM and Key from Spotify", command=self.fetch_bpm_and_key_from_spotify)
        self.fetch_bpm_button.pack(pady=10)

        self.fetch_currently_playing_button = ttk.Button(self.root, text="Fetch Currently Playing Track", command=self.fetch_currently_playing_track)
        self.fetch_currently_playing_button.pack(pady=10)

        self.key_label = ttk.Label(self.root, text="Key: N/A")
        self.key_label.pack(pady=10)
    
    def start_metronome(self):
        try:
            self.bpm = int(self.bpm_entry.get())
        except ValueError:
            return
        self.is_running = True
        self.metronome_thread = threading.Thread(target=self.run_metronome)
        self.metronome_thread.start()
    
    def stop_metronome(self):
        self.is_running = False
        if hasattr(self, 'metronome_thread'):
            self.metronome_thread.join()

    def run_metronome(self):
        interval = 60.0 / self.bpm
        while self.is_running:
            self.tick_sound.play()
            time.sleep(interval)

    def fetch_bpm_and_key_from_spotify(self):
        track_id = self.track_entry.get()
        bpm, key = self.get_track_audio_features(track_id)
        self.update_bpm_and_key(bpm, key)

    def fetch_currently_playing_track(self):
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            print("Please go to this URL and authorize the application:", auth_url)
            response = input("Paste the redirect URL here: ")
            code = sp_oauth.parse_response_code(response)
            token_info = sp_oauth.get_access_token(code)
        
        access_token = token_info['access_token']
        
        sp = spotipy.Spotify(auth=access_token)
        current_track = sp.currently_playing()
        
        if current_track is not None and current_track['is_playing']:
            track_id = current_track['item']['id']
            bpm, key = self.get_track_audio_features(track_id)
            self.update_bpm_and_key(bpm, key)
        else:
            print("No track is currently playing.")

    def get_track_audio_features(self, track_id):
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            print("Please go to this URL and authorize the application:", auth_url)
            response = input("Paste the redirect URL here: ")
            code = sp_oauth.parse_response_code(response)
            token_info = sp_oauth.get_access_token(code)
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
        audio_features = sp.audio_features(track_id)[0]
        bpm = audio_features['tempo']
        key = audio_features['key']
        return bpm, key

    def update_bpm_and_key(self, bpm, key):
        self.bpm_entry.delete(0, tk.END)
        self.bpm_entry.insert(0, str(bpm))
        self.bpm = bpm

        key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        key_name = key_names[key]
        self.key_label.config(text=f"Key: {key_name}")
        self.key = key_name

if __name__ == "__main__":
    root = tk.Tk()
    app = MetronomeApp(root)
    root.mainloop()
