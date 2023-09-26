from flask import request
from uuid import uuid4
from app import app

from database import music

@app.get('/music')
def get_music():
    return {'music': music}

@app.get('/music/<music_id>')
def get_music(music_id):
    try:
        musi = music[music_id]
        return musi, 200
    except KeyError:
        return {"message": "music not found"}, 400

@app.post('/music')
def create_music():
    music_data = request.get_json()
    music[uuid4().hex] = music_data
    return music_data, 201

@app.put('/music/<music_id>')
def edit_music(music_id):
    music_data = request.get_json()
    if music_id in music:
        musi = music[music_id]
        musi['body'] = music_data['body']
        return musi, 200
    return {"message": "music not found"}, 400


@app.delete('/music/<music_id>')
def delete_music(music_id):
    try:
        deleted_music = music.pop(music_id)
        return {'message':f"{deleted_music['body']} deleted"}, 202
    except:
        return {"message": "music not found"}, 400
