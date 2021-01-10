import helpers as spotify
from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)


@app.route('/common_songs', methods=['POST', 'GET'])
def find_common_songs():
    spotify.setup()
    data = request.args
    user1 = data.get("user1")
    user2 = data.get("user2")
    songs = spotify.get_common_songs(user1, user2, 10)
    data = spotify.get_track_names(songs)
    return render_template('songs.html', songs=data, message='You share these songs in common')

@app.route('/party_music', methods=['POST', 'GET'])
def find_party_music():
    spotify.setup()
    data = request.args
    user = data.get("user")
    playlists = spotify.get_users_playlists(user)
    danceable = spotify.get_most_danceable(playlists, 10)
    data = spotify.get_track_names([x[1] for x in danceable])
    return render_template('songs.html', songs=data, message='Here are some good tunes to dance to:')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)