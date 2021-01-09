import requests

CLIENT_ID = ''
CLIENT_SECRET = ''
AUTH_URL = 'https://accounts.spotify.com/api/token'

response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

data = response.json()
# Application access token. Not authentication for a particular user. 
access_token = data['access_token']

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

BASE_URL = 'https://api.spotify.com/v1/'

# Endpoint that returns list of all playlists objects for a user (public data)
USER_DATA_URL = BASE_URL + 'users/iamkatefrom2000/playlists'

playlists = requests.get(USER_DATA_URL, headers=headers).json()['items']
playlist_urls = []

# Each is a playlist object with attributes collaborative, description, external_urls,
# followers, href, id, images, name, owner, public, snapshot_id, tracks, type, uri
for playlist in playlists:
    playlist_url = playlist['tracks']['href']
    playlist_urls.append(playlist_url)

# paging object with attributes href, items, limit, next, offset, previous, total
playlist0 = requests.get(playlist_urls[0], headers=headers).json()
tracks = playlist0['items']

playlist_name = playlists[0]['name']

print(playlist_name)
for track in tracks:
    print(track['track']['name'])