from flask import render_template, request, flash, redirect
from musicdb import app
from app import db
from app.models import Artist,Recording,Song
from app.forms import MusicSearchForm,AlbumForm,ArtistForm
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import time

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def main():
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        print (search)
        return search_results(search)

    return render_template("index.html", form=search)


@app.route('/results')
def search_results(search):

    results = []
    print(search.select)
    search_string = search.data['search']

    print (search_string)

    if search_string:
        if search.data['select'] == 'Artist':
            print ("Doing a search on Artist=",search_string)

            qry = db.session.query(Recording,Artist).filter(Recording.artist_id==Artist.id).\
                                    filter(Artist.artist_name.contains(search_string))
            results=qry.all()

            print (results)
        elif search.data['select'] == 'Album':
            print ("Doing a search on Album=",search_string)
            qry = db.session.query(Recording,Artist).filter(Recording.artist_id==Artist.id).\
                filter(Recording.record_name.contains(search_string))
            results = qry.all()

            print(results)


    else:
        qry = db.session.query(Recording,Artist).filter(Recording.artist_id==Artist.id)
        results = qry.all()

    if not results:
        print ("No Results Found")
        flash('No results found!',category="warning")
        return redirect('/')
    else:
        # display results

        for _row in results:
            print(_row.Recording.record_name,_row.Artist.artist_name)
        return render_template('show-recordings.html', recordings=results)


@app.route('/insert')
def insert():
    artist=Artist(id="1",artist_name='Polka Country Musicians')
    db.session.add(artist)
    db.session.commit()
    print (artist)
    return str(artist)




@app.route('/show-artist')
def show_artist():
   return render_template('show-artists.html', artists = Artist.query.all() )

@app.route('/show-recording')
def show_recording():
    qry = db.session.query(Recording,Artist).filter(Recording.artist_id==Artist.id)
    results=qry.all()
    return render_template('show-recordings.html', recordings = results )

@app.route('/show-song')
def show_song():
   return render_template('show-songs.html', songs = Song.query.all() )

@app.route('/new_album', methods=['GET', 'POST'])
def new_album():
    """
    Add a new album
    """

    print ("New_Album")
    form = AlbumForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the album
        recording = Recording()

        ts = int(time.time())
        recording.id = ts
        recording.artist_id = form.artist_id
        recording.record_name = form.album_name
        recording.label_number = form.label_number
        recording.label = form.label
        recording.count_lp = form.count_lp
        recording.count_45 = form.count_45
        recording.count_78 = form.count_78
        recording.count_cassette = form.count_cassette
        recording.count_copy_cassette = form.count_copy_cassette
        recording.count_cd = form.count_cd
        recording.count_copy_cd = form.count_copy_cd
        recording.count_digital = form.count_digital

        try:
            db.session.add(recording)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            message = "ERROR: " + str(e.__dict__['orig'])
            category="danger"
        else:
            message = "Successfully Added Recording: " + recording.record_name + ", with ID: " + str(recording.id)
            category = "success"

        flash("Entering Album: "+form.album_name.data,category="success")

        return redirect('/')


    return render_template('new_album.html', form=form)


def save_changes(recording, form, new=False):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object


    recording.album_name = form.album_name.data
    recording.label = form.label.data
    recording.label_number = form.label_number.data


#    if new:
        # Add the new album to the database
        #db_session.add(album)

    # commit the data to the database
    #db_session.commit()

@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
    """
    Add a new album
    """
    form = ArtistForm(request.form)

    if request.method == 'POST' and form.validate():

        exists = Artist.query.filter(Artist.artist_name == form.artist_name.data).first()

        if exists:
            message = form.artist_name.data+" already exists in the database!"
            category="danger"
        else:


            new_artist = Artist()
            new_artist.artist_name = form.artist_name.data
            ts = int(time.time())
            new_artist.id = ts
            # save the album
            #recording = Recording()

            try:
                db.session.add(new_artist)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                message = "ERROR: "+ str(e.__dict__['orig'])
                category="danger"
            else:
                message = "Successfully Added Artist: " + new_artist.artist_name + ", with ID: "+str(new_artist.id)
                category = "success"
        #save_changes(recording, form, new=True)

        return redirect('/')

    return render_template('new_artist.html', form=form)

def save_form(form,artistid):

    recording = Recording()


    ts = int(time.time())
    recording.id = ts
    #recording.artist_id = form.artist_id.data
    recording.artist_id = artistid
    recording.record_name = form.album_name.data
    recording.label_number = form.label_number.data
    recording.label = form.label.data
    recording.type = form.label.data
    recording.cover = form.cover.data
    recording.word = form.word.data
    recording.count_lp = form.count_lp.data
    recording.count_45 = form.count_45.data
    recording.count_78 = form.count_78.data
    recording.count_cassette = form.count_cassette.data
    recording.count_copy_cassette = form.count_copy_cassette.data
    recording.count_cd = form.count_cd.data
    recording.count_copy_cd = form.count_copy_cd.data
    recording.count_digital = form.count_digital.data

    try:
        db.session.add(recording)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        message = "ERROR: " + str(e.__dict__['orig'])
        category = "danger"
    else:
        message = "Successfully Added Recording: " + recording.record_name + ", with ID: " + str(recording.id)
        category = "success"

    flash(message, category=category)


@app.route("/new_recording/<artistid>", methods=('GET', 'POST'))
def newrecording(artistid):

    print("Adding a new recording for ArtistID: "+artistid)

    form = AlbumForm(request.form)
    form.artist_id = artistid

    if request.method == 'POST' and form.validate():
        print ("Saving New Record")
        save_form(form,artistid)
        return redirect ('/')

    return render_template('new_album.html', form=form)