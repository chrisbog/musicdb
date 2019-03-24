from wtforms import Form, StringField, SelectField, IntegerField, BooleanField

class MusicSearchForm(Form):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album')]
    select = SelectField('Select a search type:', choices=choices)
    search = StringField('')

class AlbumForm(Form):

    artist_id = IntegerField("Artist ID")
    artist_name = StringField('Artist Name',render_kw={'readonly': True})
    album_name = StringField('Album Title')
    label = StringField('Label')
    label_number = StringField('Label Number')
    cover = BooleanField('Cover')
    word = BooleanField('Word')
    count_cassette = IntegerField("Cassette")
    count_lp = IntegerField("LP")
    count_45 = IntegerField("45")
    count_78 = IntegerField("78")
    count_cd = IntegerField("CD")
    count_digital = IntegerField("Digital")
    count_copy_cassette = IntegerField("Copy Cassette")
    count_copy_cd = IntegerField("Copy CD")


class ArtistForm(Form):
    artist_name = StringField('Artist')
