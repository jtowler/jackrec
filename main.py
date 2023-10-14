import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#
# from IPython.display import Image, display
# from matplotlib import pyplot as plt

sp_oauth = SpotifyOAuth(os.getenv('SPOTIPY_CLIENT_ID'),
                        os.getenv('SPOTIPY_CLIENT_SECRET'),
                        'http://localhost:8888/callback/',
                        scope='user-read-playback-state user-modify-playback-state streaming')

code = sp_oauth.get_auth_response()
token = sp_oauth.get_access_token(code)

refresh_token = token['refresh_token']
client = spotipy.Spotify(auth=token['access_token'])

currently_playing = client.current_playback()

device = currently_playing['device']['id']
album = currently_playing['item']['album']
artist = album['artists'][0]
artist_name = artist['name']
artist_id = artist['id']
title = album['name']
image = album['images'][1]['url']
# Image(url=image)

artist_albums = client.artist_albums(artist_id)
more_albums = [[item['id'], item['name'], item['images'][-1]['url']] for item in artist_albums['items']]

for i, (_id, name, url) in enumerate(more_albums):
    # display(Image(url=url))
    print(i, name)

selected_index = int(input('Make selection: '))
selected_album_id = more_albums[selected_index][0]

selected_album = client.album(selected_album_id)

client.start_playback(device_id=device, context_uri=selected_album['uri'])
