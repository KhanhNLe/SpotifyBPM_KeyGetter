import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pygame
import threading
import webbrowser
import json

class MetronomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Metronome")
        self.track_id_visible = False
        self.credentials_file = "spotify_credentials.json"
        self.is_running = False
        self.metronome_sound_file = "tick.wav"  # Default metronome sound
        self.metronome_volume = 1.0  # Default volume (100%)
        self.current_track_id = None  # Track ID to detect changes

        # Set up the closing protocol to handle cleanup
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize the application
        self.init_app()

    
    def init_app(self):
        credentials = self.read_credentials()

        if not credentials:
            print("Spotify API credentials are not set in the credentials file.")
            self.credentials_window()
            return

        client_id = credentials.get('SPOTIPY_CLIENT_ID')
        client_secret = credentials.get('SPOTIPY_CLIENT_SECRET')
        redirect_uri = credentials.get('SPOTIPY_REDIRECT_URI')

        print(f"SPOTIPY_CLIENT_ID: {client_id}")
        print(f"SPOTIPY_CLIENT_SECRET: {client_secret}")
        print(f"SPOTIPY_REDIRECT_URI: {redirect_uri}")

        print("Initializing Spotify OAuth")
        self.sp_oauth = SpotifyOAuth(client_id=client_id,
                                     client_secret=client_secret,
                                     redirect_uri=redirect_uri,
                                     scope="user-read-playback-state user-library-read")

        self.sp = spotipy.Spotify(auth_manager=self.sp_oauth)
        
        self.setup_gui()
        self.fetch_currently_playing_track()

    def read_credentials(self):
        try:
            with open(self.credentials_file, 'r') as file:
                credentials = json.load(file)
            return credentials
        except FileNotFoundError:
            return None

    def save_credentials(self, client_id, client_secret, redirect_uri):
        credentials = {
            'SPOTIPY_CLIENT_ID': client_id,
            'SPOTIPY_CLIENT_SECRET': client_secret,
            'SPOTIPY_REDIRECT_URI': redirect_uri
        }
        with open(self.credentials_file, 'w') as file:
            json.dump(credentials, file)
        print("Credentials saved to file.")

    def credentials_window(self):
        self.cred_window = tk.Toplevel(self.root)
        self.cred_window.title("Enter Spotify Credentials")

        tk.Label(self.cred_window, text="Client ID:").grid(row=0, column=0)
        self.client_id_entry = tk.Entry(self.cred_window)
        self.client_id_entry.grid(row=0, column=1)

        tk.Label(self.cred_window, text="Client Secret:").grid(row=1, column=0)
        self.client_secret_entry = tk.Entry(self.cred_window)
        self.client_secret_entry.grid(row=1, column=1)

        tk.Label(self.cred_window, text="Redirect URI:").grid(row=2, column=0)
        self.redirect_uri_entry = tk.Entry(self.cred_window)
        self.redirect_uri_entry.grid(row=2, column=1)

        tk.Button(self.cred_window, text="Save", command=self.save_credentials_from_window).grid(row=3, columnspan=2)

    def save_credentials_from_window(self):
        client_id = self.client_id_entry.get()
        client_secret = self.client_secret_entry.get()
        redirect_uri = self.redirect_uri_entry.get()
        self.save_credentials(client_id, client_secret, redirect_uri)
        self.cred_window.destroy()
        self.init_app()

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

        self.setup_gui()
        self.fetch_currently_playing_track()  # Start the dynamic checker

    def start_metronome(self):
        if not self.is_running:
            self.is_running = True
            print("Starting metronome...")
            self.metronome_thread = threading.Thread(target=self.run_metronome)
            self.metronome_thread.start()

    def run_metronome(self):
        while self.is_running:
            if self.metronome_sound_file:
                try:
                    print(f"Loading metronome sound: {self.metronome_sound_file}")
                    pygame.mixer.music.load(self.metronome_sound_file)
                    pygame.mixer.music.set_volume(self.volume_slider.get())
                    pygame.mixer.music.play()
                    pygame.time.wait(int(60000 / self.bpm))  # Wait for the duration of one beat
                except pygame.error as e:
                    print(f"Error playing metronome sound: {e}")
                    self.stop_metronome()

    def stop_metronome(self):
        if self.is_running:
            self.is_running = False
            print("Stopping metronome...")
            if hasattr(self, 'metronome_thread'):
                self.metronome_thread.join()  # Wait for the thread to finish
            pygame.mixer.music.stop()
            print("Metronome stopped.")

    def show_track_info(self):
        self.track_name_label.pack()
        self.key_label.pack()
        self.track_id_visible = True

    def hide_track_info(self):
        self.track_name_label.pack_forget()
        self.key_label.pack_forget()
        self.track_id_visible = False


    def setup_gui(self):
        # Frame for Metronome Control
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(padx=10, pady=10)
        
        
        # Metronome sound file selection
        self.sound_file_button = tk.Button(self.root, text="Select Metronome Sound", command=self.select_sound_file)
        self.sound_file_button.pack()

        # Metronome volume control
        self.volume_slider = tk.Scale(controls_frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, label="Volume")
        self.volume_slider.set(self.metronome_volume)
        self.volume_slider.grid(row=0, column=1, padx=5, pady=5)
        
        # Other GUI elements...
        self.track_name_label = tk.Label(self.root, text="Track: None")
        self.track_name_label.pack()

        # BPM label and entry
        self.bpm_label = tk.Label(controls_frame, text="BPM:")
        self.bpm_label.grid(row=2, column=0, padx=5, pady=5)

        self.bpm_entry = tk.Entry(controls_frame, state='readonly')
        self.bpm_entry.grid(row=2, column=1, padx=5, pady=5)
        self.bpm_entry.insert(0, "N/A")  # Set initial placeholder value

        self.key_label = tk.Label(self.root, text="Key:")
        self.key_label.pack()

        # Initialize pygame for sound playback
        pygame.mixer.init()

    def select_sound_file(self):
        self.metronome_sound_file = filedialog.askopenfilename(
            title="Select Metronome Sound",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        print(f"Selected sound file: {self.metronome_sound_file}")

    def fetch_currently_playing_track(self):
        try:
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
                elif not self.is_running:
                    self.start_metronome()  # Resume metronome if it was stopped
            else:
                self.stop_metronome()  # Stop the metronome if no track is playing
        except Exception as e:
            print(f"Error fetching currently playing track: {e}")
        
        self.root.after(500, self.fetch_currently_playing_track)  # Check every .5 second
        
    def get_track_audio_features(self, track_id):
        audio_features = self.sp.audio_features(track_id)[0]
        bpm = round(audio_features['tempo'])  # Round the BPM value
        key = audio_features['key']
        return bpm, key

    def update_bpm_and_key(self, bpm, key):
        self.bpm_entry.config(state=tk.NORMAL)  # Temporarily make it editable
        self.bpm_entry.delete(0, tk.END)
        self.bpm_entry.insert(0, str(bpm))  # Insert fetched BPM
        self.bpm_entry.config(state='readonly')  # Set it back to readonly
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
