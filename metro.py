import tkinter as tk
from tkinter import ttk, messagebox
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pygame
import threading
import webbrowser
import os

class MetronomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Metronome")
        self.track_id_visible = False

        # Uncomment the next line to test caching by wiping the token
        # self.wipe_cached_token()

        # Set up the closing protocol to handle cleanup
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize the application
        self.init_app()

    def wipe_cached_token(self):
        try:
            os.remove(".spotify_cache")
            print("Cached token file removed.")
        except FileNotFoundError:
            print("No cached token file found to remove.")

    def init_app(self):
        # Retrieve credentials from environment variables
        client_id = os.getenv('SPOTIPY_CLIENT_ID')
        client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

        # Validate that the environment variables are set
        if not client_id or not client_secret or not redirect_uri:
            print("Spotify API credentials are not set in the environment variables.")
            self.credentials_window()
            return

        print("Initializing Spotify OAuth")
        # Set up the Spotify OAuth object with caching
        self.sp_oauth = SpotifyOAuth(client_id=client_id,
                                     client_secret=client_secret,
                                     redirect_uri=redirect_uri,
                                     scope="user-read-playback-state user-library-read",
                                     cache_path=".spotify_cache")

        # Check for a cached token
        self.check_cached_token()

    def credentials_window(self):
        self.cred_window = tk.Toplevel(self.root)
        self.cred_window.title("Enter Spotify Credentials")

        ttk.Label(self.cred_window, text="Client ID:").pack(pady=5)
        self.client_id_entry = ttk.Entry(self.cred_window, width=40)
        self.client_id_entry.pack(pady=5)

        ttk.Label(self.cred_window, text="Client Secret:").pack(pady=5)
        self.client_secret_entry = ttk.Entry(self.cred_window, width=40, show="*")
        self.client_secret_entry.pack(pady=5)

        ttk.Label(self.cred_window, text="Redirect URI:").pack(pady=5)
        self.redirect_uri_entry = ttk.Entry(self.cred_window, width=40)
        self.redirect_uri_entry.pack(pady=5)
        self.redirect_uri_entry.insert(0, "http://localhost:8888/callback")

        submit_button = ttk.Button(self.cred_window, text="Submit", command=self.set_credentials)
        submit_button.pack(pady=10)

    def set_credentials(self):
        client_id = self.client_id_entry.get()
        client_secret = self.client_secret_entry.get()
        redirect_uri = self.redirect_uri_entry.get()

        if not client_id or not client_secret or not redirect_uri:
            messagebox.showerror("Error", "All fields are required!")
            return

        os.environ['SPOTIPY_CLIENT_ID'] = client_id
        os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
        os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri

        self.cred_window.destroy()

        # Re-initialize the application with the new credentials
        self.init_app()

    def check_cached_token(self):
        token_info = self.sp_oauth.get_cached_token()
        print(f"Cached token: {token_info}")

        if not token_info:
            print("No cached token found, proceeding with authorization.")
            self.authorize_spotify()
        else:
            print("Using cached token.")
            self.sp = spotipy.Spotify(auth=token_info['access_token'])
            self.complete_initialization()

    def authorize_spotify(self):
        auth_url = self.sp_oauth.get_authorize_url()
        print(f"Auth URL: {auth_url}")
        self.oauth_window = tk.Toplevel(self.root)
        self.oauth_window.title("Spotify Authorization")

        label = ttk.Label(self.oauth_window, text="Please authorize the application:")
        label.pack(pady=10)

        auth_button = ttk.Button(self.oauth_window, text="Authorize", command=lambda: self.open_browser(auth_url))
        auth_button.pack(pady=10)

        self.redirect_entry = ttk.Entry(self.oauth_window, width=50)
        self.redirect_entry.pack(pady=10)
        self.redirect_entry.insert(0, "Paste the redirect URL here")

        submit_button = ttk.Button(self.oauth_window, text="Submit", command=self.get_token)
        submit_button.pack(pady=10)

    def open_browser(self, url):
        webbrowser.open(url)

    def get_token(self):
        response = self.redirect_entry.get()
        print(f"Redirect response: {response}")
        code = self.sp_oauth.parse_response_code(response)
        token_info = self.sp_oauth.get_access_token(code)
        print(f"New token: {token_info}")
        self.sp = spotipy.Spotify(auth=token_info['access_token'])
        messagebox.showinfo("Success", "Spotify authorization successful!")
        self.oauth_window.destroy()
        self.complete_initialization()

    def complete_initialization(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        self.tick_sound = pygame.mixer.Sound("tick.wav")  # Ensure you have a tick.wav file in the same directory

        self.bpm = 60
        self.key = None
        self.is_running = False
        self.current_track_id = None

        self.create_widgets()
        self.hide_track_info()  # Call Hide_Track_Info

        self.fetch_currently_playing_track()  # Start the dynamic checker

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

        # Add a hide button
        self.hide_track_info_button = ttk.Button(self.root, text="Hide Track Info", command=self.hide_track_info)
        self.hide_track_info_button.pack(pady=10)

        # Add a show button
        self.show_track_info_button = ttk.Button(self.root, text="Show Track Info", command=self.show_track_info)
        self.show_track_info_button.pack(pady=10)

        self.track_name_label = ttk.Label(self.root, text="")
        self.track_name_label.pack(pady=10)

        self.key_label = ttk.Label(self.root, text="")
        self.key_label.pack(pady=10)

    def start_metronome(self):
        if not self.is_running:
            self.is_running = True
            self.metronome_thread = threading.Thread(target=self.run_metronome)
            self.metronome_thread.start()

    def run_metronome(self):
        while self.is_running:
            pygame.mixer.Sound.play(self.tick_sound)
            pygame.time.wait(int(60000 / self.bpm))

    def stop_metronome(self):
        self.is_running = False

    def show_track_info(self):
        self.track_name_label.pack()
        self.key_label.pack()
        self.track_id_visible = True

    def hide_track_info(self):
        self.track_name_label.pack_forget()
        self.key_label.pack_forget()
        self.track_id_visible = False

    def fetch_currently_playing_track(self):
        if not hasattr(self, 'sp'):
            return

        current_playback = self.sp.current_playback()
        if current_playback and current_playback['is_playing']:
            track_id = current_playback['item']['id']
            track_name = current_playback['item']['name']
            artist_name = current_playback['item']['artists'][0]['name']
            if track_id != self.current_track_id:
                self.current_track_id = track_id
                bpm, key = self.get_track_audio_features(track_id)
                self.update_bpm_and_key(bpm, key)
                self.update_track_name(track_name, artist_name)
                self.start_metronome()  # Start metronome after fetching BPM and key
        else:
            print("No track is currently playing.")
        
        # Schedule the next check
        self.root.after(1000, self.fetch_currently_playing_track)  # Check every 1 second

    def get_track_audio_features(self, track_id):
        audio_features = self.sp.audio_features(track_id)[0]
        bpm = round(audio_features['tempo'])  # Round the BPM value
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
        
    def update_track_name(self, track_name, artist_name):
        self.track_name_label.config(text=f"Track: {track_name} by {artist_name}")

    def on_closing(self):
        # Stop the metronome if it's running
        if self.is_running:
            self.is_running = False
            if hasattr(self, 'metronome_thread'):
                self.metronome_thread.join()  # Wait for the thread to finish

        # Close the application window
        self.root.destroy()
        print("Application closed.")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MetronomeApp(root)
    root.mainloop()
