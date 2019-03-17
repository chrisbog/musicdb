from wtforms import Form, StringField, SelectField

class MusicSearchForm(Form):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')

class AlbumForm(Form):
    album_name = StringField('Album Title')
    label = StringField('Label')
    label_number = StringField('Label Number')

class ArtistForm(Form):
    artist_name = StringField('Artist')
