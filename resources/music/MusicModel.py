from app import database
from datetime import datetime

class MusicModel(database.Model):
    __tablename__ = 'music'

    id = database.Column(database.Integer, primary_key = True)
    body = database.Column(database.String, nullable = False)
    timestamp = database.Column(database.String, default = datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey('artists.id'), nullable = False)

    def __repr__(self):
        return f'<Music: {self.body}>'
    
    def save(self):
        database.session.add(self)
        database.session.commit()
        
    def delete(self):
        database.session.delete(self)
        database.session.commit()