import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "e493958b18d8498a8a56b5fa6698d0ef"
CLIENT_SECRET = "bc43cd76140d4ebc85f1f89020a7d5ae"

date = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, "html.parser")

top_songs = soup.select(selector="li ul li h3", class_="c-title", id="title-of-a-story")

top_songs_list = [song.getText().strip() for song in top_songs]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://localhost/8080",
                                               scope="playlist-modify-private"))
uri_list = []
for song in top_songs_list:
    try:
        track_data = sp.search(q=f"track: {song} year: {date[:4]}", type="track")
        if song not in uri_list:
            uri_list.append(track_data['tracks']['items'][0]['uri'])
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(uri_list)
print(len(uri_list))
user = sp.current_user()
user_id = user["id"]

response = sp.user_playlist_create(user=user_id, name=date, public=False, collaborative=False, description="time capsule")
playlist_id = response['id']

sp.playlist_add_items(playlist_id=playlist_id, items=uri_list, position=None)
