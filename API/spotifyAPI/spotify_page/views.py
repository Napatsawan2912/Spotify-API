from django.conf import settings
from django.shortcuts import render
import requests
import random
from requests.auth import HTTPBasicAuth

TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=50'


def get_api_token():
    data = {
        "grant_type": "client_credentials"
    }
    auth_response = requests.post(TOKEN_URL, data=data, auth=HTTPBasicAuth(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET))

    if auth_response.status_code == 200:
        auth_response_data = auth_response.json()["access_token"]
        return auth_response_data
    else:
        raise Exception(f"Failed to obtain token: {auth_response.status_code}, {auth_response.text}")


def get_spotify(request):
    API_TOKEN = get_api_token()  # Get a new API token

    mood = request.GET.get('mood', 'love')  # default to 'love' if no mood is selected

    # Map mood to playlist IDs (example playlist IDs)
    mood_playlists = {
        'love': '3zVeVhkn4LEpe6EDUZNNhq',  # Example playlist ID for 'love'
        'miss': '1HQR3ZaPPvyyFm01Vb26gt',  # Example playlist ID for 'miss'
        'sad': '0u5ZmdixnCw14EboDDm7rE',   # Example playlist ID for 'sad'
        'chill': '5o3mULJ7Ko9aVfoNwRBSxg',  # Example playlist ID for 'chill'
        'cute': '0DNcE1tGpVnK9D64c6xkdo',   # Example playlist ID for 'cute'
    }

    playlist_id = mood_playlists.get(mood, '3zVeVhkn4LEpe6EDUZNNhq')  # default to 'love'
    url = BASE_URL.format(playlist_id=playlist_id)

    headers = {
        'Authorization': f'Bearer {API_TOKEN}'
    }

    response = requests.get(url, headers=headers)
    context = {
        'songs': [],
        'welcome': f"Welcome to T-POP! Mood: {mood.capitalize()}"
    }

    if response.status_code == 200:
        data = response.json()
        songs = []
        items = data['items']

        random.shuffle(items)
        selected_songs = items[:3]

        for item in selected_songs:
            track = item['track']
            album = track['album']

            song = {
                'images': album['images'][0]['url'],
                'name': track['name'],
                'artists': track['artists'][0]['name'],
                'artists_url': track['artists'][0]["external_urls"]["spotify"],
                'song_url': track['external_urls']['spotify']
            }

            songs.append(song)

        context['songs'] = songs

    else:
        print(f"Error: {response.status_code}, Not Found.")

    return render(request, "spotify_page/spotify-app.html", context)
