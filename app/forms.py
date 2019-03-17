from wtforms import Form, StringField, SelectField

class MusicSearchForm(Form):
    choices = [('Artist', 'Artist'),
               ('Album', 'Album')]
    select = SelectField('Search for music:', choices=choices)
    search = StringField('')