from app import app


@app.get('/music')
def get_music():
    pass

@app.post('/music')
def create_music():
    pass

@app.put('/music')
def edit_music():
    pass

@app.delete('/music')
def delete_music():
    pass
