Key Features:

Metronome Functionality: The app offers a robust metronome tool that allows musicians to set and adjust tempo (BPM) easily.

Integration with Spotify: Users can seamlessly fetch BPM and track key information from Spotify, enhancing practice sessions with accurate musical data.

User Interface: Designed with simplicity in mind, the app features a user-friendly interface using Tkinter for desktop use, providing intuitive controls for musicians of all skill levels.

How It Works:

Users authenticate their Spotify account through OAuth, enabling the app to access Spotify's vast music database.

Upon selecting the "Fetch BPM and Key" button, the app queries Spotify for real-time BPM and key information of the currently playing track, displaying it instantly.

Musicians benefit from precise tempo guidance and musical key insights directly integrated into their practice environment.

Future Enhancements:

Planned expansions include mobile compatibility, allowing users to access the metronome and Spotify integration on-the-go through iOS or Android devices.

Integration of additional Spotify features such as playlist management and audio playback control to further enrich the user experience.

This collaborative project highlights the intersection of music practice tools and API integration, providing a tailored solution for musicians seeking enhanced practice sessions and musical insights.


Usage:
Log into Spotify Developer Dashboard
Go to Spotify Developer Dashboard.
Log in with your Spotify account credentials.
Select Your Application
If you haven't already created an application, you'll need to create one before proceeding.
After Creation
It should list Your
1. Client ID
2. View Secret ID to show your Secret ID

Setting Redirect URI
Go to your Spotify Developer Dashboard:
Log in to your Spotify Developer account.
Open your application settings.
Set the Redirect URI:
In your app settings, find the Redirect URIs section.
Add http://localhost:8888/callback (or any other appropriate URL) as your Redirect URI.

Edit the script via your favorite IDE:
Copy and paste the IDs into their respectively slot, including your Redirect URI

Save
Run Script
Look at Terminal, copy-paste link into google.com
Should ask for your authorization
I usually get a 404 page here, but that's okay just copy and paste the url after the 404 screen into terminal. 
Everything should work, if you have spotify installed already.
Have Fun Practicing!
