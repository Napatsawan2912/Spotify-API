from django.conf import settings
from django.shortcuts import render
import requests
import random

TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=50'


def get_api_token():
    auth_response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'client_credentials',
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        }
    )

    if auth_response.status_code == 200:
        auth_response_data = auth_response.json()
        return auth_response_data['access_token']
    else:
        raise Exception(f"Failed to obtain token: {auth_response.status_code}, {auth_response.text}")


def get_spotify(request):
    API_TOKEN = get_api_token()  # Get a new API token

    mood = request.GET.get('mood', 'love')  # default to 'love' if no mood is selected

    # Map mood to playlist IDs (example playlist IDs)
    mood_playlists = {
        'love': '37i9dQZF1DX2wrHNWlb0Eu',  # Example playlist ID for 'love'
        'miss': '37i9dQZF1DX7wnCfGfUD8C',  # Example playlist ID for 'miss'
        'sad': '37i9dQZF1DX4tHo2ftQyun',   # Example playlist ID for 'sad'
        'chill': '37i9dQZF1DX0bGxKepv6YZ',  # Example playlist ID for 'chill'
        'cute': '37i9dQZF1DWZRLdKC8qik7',   # Example playlist ID for 'cute'
    }

    playlist_id = mood_playlists.get(mood, '37i9dQZF1DX2wrHNWlb0Eu')  # default to 'love'
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
