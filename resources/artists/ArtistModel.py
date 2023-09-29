from app import database
from werkzeug.security import generate_password_hash, check_password_hash

# class FollowersModel(database.Model):
#     id = database.Column(database.Integer, primary_key = True)
#     username = database.Column(database.String, unique = True, nullable = False)
#     email = database.Column(database.String, unique = True, nullable = False)

followers = database.Table('followers', 
    database.Column('follower_id', database.Integer, database.ForeignKey('artists.id')),                       
    database.Column('followed_id', database.Integer, database.ForeignKey('artists.id')))

class ArtistModel(database.Model):

    __tablename__ = 'artists'

    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String, unique = True, nullable = False)
    email = database.Column(database.String, unique = True, nullable = False)
    password_hash = database.Column(database.String, nullable = False)
    first_name = database.Column(database.String)
    last_name = database.Column(database.String)
    music = database.relationship('MusicModel', backref='author', lazy='dynamic', cascade='all, delete')
    followed = database.relationship('ArtistModel',
        secondary=followers,
        primaryjoin=followers.c.follower_id == id,
        secondaryjoin = followers.c.followed_id == id,
        backref = database.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<Artist: {self.username}>'
    
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

    def is_following(self, artist):
        self.followed.filter(artist.id == followers.c.followed_id).count() > 0

    def follow_user(self, artist):
        if not self.is_following(artist):
            self.followed.append(artist)
            self.save()
    
    def unfollow_user(self, artist):
        if self.is_following(artist):
            self.followed.remove(artist)
            self.save()