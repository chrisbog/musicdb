from app import db

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(80), index=True, unique=True)
    #recordings = db.relationship('Recording', backref='artist',lazy='dynamic')

    def __repr__(self):
        return '<Artist id={}, name={}>'.format(self.id,self.artist_name)

class Recording(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    record_name = db.Column(db.String(80), index=True, unique=False)
    label = db.Column(db.String(20))
    label_number = db.Column(db.String(20))
    type = db.Column(db.Integer)
    cover = db.Column(db.Boolean)
    word = db.Column(db.Boolean)
    count_cassette = db.Column(db.Integer)
    count_lp = db.Column(db.Integer)
    count_45 = db.Column(db.Integer)
    count_78 = db.Column(db.Integer)
    count_cd = db.Column(db.Integer)
    count_digital  = db.Column(db.Integer)
    count_copy_cassette = db.Column(db.Integer)
    count_copy_cd = db.Column(db.Integer)
    artist_id = db.Column(db.Integer,db.ForeignKey('artist.id'))
    #songs = db.relationship('Song',backref='recording',lazy='dynamic')

    def __repr__(self):
        return '<Recording {}>'.format(self.record_name)

class Song(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    song_name = db.Column(db.String(35))
    record_id = db.Column(db.Integer, db.ForeignKey('recording.id'))

    def __repr__(self):
        return '<Song ID {},Record ID: {}, Song Name: {}>'.format(self.id,self.record_id, self.song_name)