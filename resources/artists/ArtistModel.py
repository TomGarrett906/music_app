from app import database
from werkzeug.security import generate_password_hash, check_password_hash

class ArtistModel(database.Model):   
    __tablename__ = 'artists'

    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String, unique = True, nullable = False)
    email = database.Column(database.String, unique = True, nullable = False)
    password_hash = database.Column(database.String, nullable = False)
    first_name = database.Column(database.String)
    last_name = database.Column(database.String)

    def __repr__(self):
        return f'<Artist: {self.username}'
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def from_dict(self, dict):
        password = dict.pop('password')
        self.hash_password(password)
        for k, v in dict.items():
            setattr(self, k, v)

    def save(self):
        database.session.add(self)
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()