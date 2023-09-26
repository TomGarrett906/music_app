from flask import request
from uuid import uuid4

from app import app
from database import artists, music


@app.get('/artist')
def get_artists():
    return {'artists': artists}, 200

@app.get('/artist/<artist_id>')
def get_artist(artist_id):
    try:
        artist = artists[artist_id]
        return artist, 200
    except KeyError:
        return {"message": "artist not found"}, 400
    

@app.post('/artist')
def create_artist():
    artist_data = request.get_json()
    artists[uuid4().hex] = artist_data
    return artist_data, 201


@app.put('/artist/<artist_id>')
def update_artist(artist_id):
    artist_data = request.get_json()
    try:
        artist = artists[artist_id]
        artist['username'] = artist_data['username']
        return artist, 200
    except KeyError:
        return {"message": "artist not found"}, 400


@app.delete('/artist/<artist_id>')
def delete_artist():
    artist_data = request.get_json()
    for a, artist in enumerate(artists):
        if artist["username"] == artist_data["username"]: artists.pop(a)
    return {"message": f"{artist_data['username']} deleted"}, 202


@app.get('/artist/<artist_id>/music')
def get_artist_music(artist_id):
    if artist_id not in artists:
        return {"message": "artist not found"}, 400
    artist_music = [musi for musi in music.values() if musi['artist_id'] == artist_id]
    return artist_music, 200

