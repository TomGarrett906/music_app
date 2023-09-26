from flask import request

from app import app
from database import artists


@app.get('/artist')
def get_artists():
    return {'artists': artists}, 200

@app.post('/artist')
def create_artist():
    artist_data = request.get_json()
    artist_data['posts'] = []
    artists.append(artist_data)
    return artist_data, 201


@app.put('/artist')
def update_artist():
    artist_data = request.get_json()
    artist = list(filter(lambda artist: artist["username"] == artist_data["username"], artists))[0]
    artist["username"] = artist_data['new username']
    return artist, 200


@app.delete('/artist')
def delete_artist():
    artist_data = request.get_json()
    for a, artist in enumerate(artists):
        if artist["username"] == artist_data["username"]: artists.pop(a)
    return {"message": f"{artist_data['username']} deleted"}, 202
