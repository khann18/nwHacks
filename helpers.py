import json
import requests
import math

headers = {}
BASE_URL = 'https://api.spotify.com/v1/'

def get_audio_features(track_id):
    AUDIO_FEATURES_URL = BASE_URL + 'audio-features/' + track_id
    return requests.get(AUDIO_FEATURES_URL, headers=headers).json()

def get_audio_features_for_track_list(track_list_for_req):
    ending = ",".join(track_list_for_req)
    AUDIO_FEATURES_URL = BASE_URL + 'audio-features/?ids=' + ending
    return requests.get(AUDIO_FEATURES_URL, headers=headers).json()

def get_track_list(playlist_obj):
    playlist_url = playlist_obj['tracks']['href']
    playlist = requests.get(playlist_url, headers=headers).json()['items']
    return playlist

# Use track ID to access the audio features, one of which is dancability
# All audio features: duration_ms, key, mode, time_signature, acousticness, danceability, energy, 
# instramentalness, liveness, loudness, speechiness, valence, tempo, id, uri, track_href, analysis_url, type
def get_most_danceable(playlist_objects, N):
    danceability_track_id_list = []
    most_danceable = {}
    # Each is a playlist object with attributes collaborative, description, external_urls,
    # followers, href, id, images, name, owner, public, snapshot_id, tracks, type, uri
    for playlist_obj in playlist_objects:   
        track_list = get_track_list(playlist_obj)
        track_list_for_req = []
        for track in track_list:
            if track and track['track'] and track['track']['id']:
                track_id = track['track']['id']
                track_list_for_req.append(track_id)
        for i in range(0, math.ceil(len(track_list) / 100)):
            audio_features_list = get_audio_features_for_track_list(track_list_for_req[i*100:i*100+100])
            for audio_features in audio_features_list['audio_features']:
                if audio_features:
                    danceability = audio_features['danceability']
                    energy = audio_features['energy']
                    id = audio_features['id']
                    if danceability and energy and id and id not in [x[1] for x in danceability_track_id_list]:
                        danceability_track_id_list.append((danceability + energy, id))

    danceability_track_id_list.sort(reverse = True)
    
    return danceability_track_id_list[0:N]
                    

            
def get_common_songs(user1, user2, num_songs):
    tracks1 = get_tracks_on_public_playlists(user1)
    tracks2 = get_tracks_on_public_playlists(user2)
    common_songs = [track for track in tracks1 if track in tracks2]
    return common_songs[0:num_songs]


def print_track_names(track_list):
    URL = 'https://api.spotify.com/v1/tracks/'
    if len(track_list) == 0:
        print("No public playlists.")
    for track_id in track_list:
        song = requests.get(URL + track_id, headers=headers).json()
        print(f"{song['name']}     by: {song['artists'][0]['name']}")

def get_track_names(track_list):
    names = []
    URL = 'https://api.spotify.com/v1/tracks/'
    if len(track_list) == 0:
        print("No public playlists.")
    for track_id in track_list:
        song = requests.get(URL + track_id, headers=headers).json()
        names.append(song['name'] + " - " + song['artists'][0]['name'])
    
    return names


def get_users_playlists(user_id):
    USER_DATA_URL = BASE_URL + 'users/'+ user_id + '/playlists'
    playlists = requests.get(USER_DATA_URL, headers=headers).json()['items']
    return playlists    

def get_tracks_on_public_playlists(user_id):
    playlist_objects = get_users_playlists(user_id)
    track_ids = []
    for playlist_object in playlist_objects:
        track_list = get_track_list(playlist_object)
        for track in track_list:
            if track and track['track'] and track['track']['id']:
                track_id = track['track']['id']
                track_ids.append(track_id)

    return track_ids
        
def get_access_token(client_id, client_secret):
    CLIENT_ID = client_id
    CLIENT_SECRET = client_secret
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    data = response.json()
    # Application access token. Not authentication for a particular user. 
    access_token = data['access_token']
    return access_token


def setup():
    client_id = '9c2816c9c9a24fc1a51112fd59c74133'
    client_secret = ''
    access_token = get_access_token(client_id, client_secret)
    global headers
    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
    }

   