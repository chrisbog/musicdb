from flask import render_template, request, flash, redirect
from musicdb import app
from app import db
from app.models import Artist,Recording,Song
from app.forms import MusicSearchForm,AlbumForm,ArtistForm
from sqlalchemy.exc import SQLAlchemyError
import time, datetime
import uuid

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def main():
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        print (search)
        return search_results(search)

    artistcount = db.session.query(Artist).count()
    recordcount = db.session.query(Recording).count()
    songcount = db.session.query(Song).count()
    return render_template("index.html", form=search, recordcount=recordcount, artistcount=artistcount,
                           songcount=songcount)


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

@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
    """
    This function will add a new Artist to the database

    :param none:
    :returns: new_album HTML Template to add the new userl
    :raises none
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

        return redirect('/')

    return render_template('new_artist.html', form=form)

def save_form(form,artistid):
    """
    This function will save the data when adding a new recording

    :param form: The form object that we defined
    :param artistid: The artist id that we want to add a recording it
    :returns: Boolean value if the insertion was successful
    :raises none
    """
    recording = Recording()

    ts = int(time.time())
    recording.id = ts

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

        songs = form.songs.data.splitlines()
        for i in songs:
            temp = Song()
            temp.record_id = recording.id
            temp.song_name = i
            temp.id = time.strftime("%Y%j%H%M")+str(time.process_time_ns()//1000)
            print(temp)
            db.session.add(temp)

        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        message = "ERROR: " + str(e.__dict__['orig'])
        category = "danger"
        rc = False
    else:
        message = "Successfully Added Recording: " + recording.record_name + ", with ID: " + str(recording.id)
        category = "success"
        rc = True

    flash(message, category=category)

    return(rc)


@app.route("/new_recording/<artistid>", methods=('GET', 'POST'))
def newrecording(artistid):
    """
    This function will create the HTML page to add a new recording given an artist ID.

    :param artistid: The ID of the Artist
    :returns: new_album HTML Template to add the new user
    :raises none
    """
    qry = db.session.query(Artist).filter(Artist.id == artistid)
    results = qry.first()
    if results:

        print("Adding a new recording for ArtistID: "+artistid+", "+str(results.artist_name))

        form = AlbumForm(request.form)
        form.artist_id.data = artistid
        form.artist_name.data = results.artist_name


        if request.method == 'POST' and form.validate():
            print ("Saving New Record")
            save_form(form,artistid)
            return redirect ('/')

        return render_template('new_album.html', form=form, artistname=results.artist_name)
    else:
        message = "Unable to add recording to Artist ID " + artistid + ". Artist doesn't exist, please add a new artist!"
        category = "danger"
        flash(message, category=category)
        return redirect ('/')

@app.route("/view_recording/<recordid>", methods=('GET', 'POST'))
def viewrecordingdetails(recordid):
    print (recordid)




    qry = db.session.query(Recording).filter(Recording.id == recordid)
    results = qry.first()

    form = AlbumForm()

    form.album_name.data = results.record_name
    form.label_number.data = results.label_number
    form.label.data = results.label
    form.label.data = results.type
    form.cover.data = results.cover
    form.word.data = results.word
    form.count_lp.data = results.word
    form.count_45.data = results.word
    form.count_78.data = results.word
    form.count_cassette.data = results.count_cassette
    form.count_copy_cassette.data = results.count_copy_cassette
    form.count_cd.data = results.count_cd
    form.count_copy_cd.data = results.count_copy_cd
    form.count_digital.data = results.count_digital



    qry = db.session.query(Artist).filter(Artist.id == results.artist_id)
    results = qry.first()

    return render_template('album-details.html', form=form, artistname=results.artist_name)
