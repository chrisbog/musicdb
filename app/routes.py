from flask import render_template, request, flash, redirect
from musicdb import app
from app import db
from app.models import Artist,Recording,Song
from app.forms import MusicSearchForm,AlbumForm,ArtistForm,SetupForm
from sqlalchemy.exc import SQLAlchemyError
from app.utils import generate_uniqueID
import time
import logging

#Global Data to Persist Between Function Calls
global_album_storage=[]


@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def main():
    """
    This function will create the HTML page to render the home page

    :param none
    :returns: index.html HTML Template which represents the home page
    :raises none
    """

    logging.debug(f"Entering main")

    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    artistcount = db.session.query(Artist).count()
    recordcount = db.session.query(Recording).count()
    songcount = db.session.query(Song).count()

    return render_template("index.html", form=search, recordcount=recordcount, artistcount=artistcount,
                           songcount=songcount)


@app.route('/results')
def search_results(search):
    """
    This function will create the HTML page to render the search results page

    :param search: represents the Search form that was populated
    :returns: show-recordings.html HTML Template which represents the search results home page
    :raises none
    """
    logging.debug(f"Entering search_results")
    results = []
    logging.debug(search.select)
    search_string = search.data['search']

    logging.debug(search_string)

    if search_string:
        if search.data['select'] == 'Artist':
            logging.info(f"Doing a search on Artist='{search_string}'")

            qry = db.session.query(Recording,Artist).filter(Recording.artist_id==Artist.id).\
                                    filter(Artist.artist_name.contains(search_string))
            results=qry.all()


        elif search.data['select'] == 'Album':
            logging.info(f"Doing a search on Album='{search_string}'")
            qry = db.session.query(Recording,Artist).filter(Recording.artist_id==Artist.id).\
                filter(Recording.record_name.contains(search_string))
            results = qry.all()

        elif search.data['select'] == 'Song':
            logging.info(f"Doing a search on Song='{search_string}'")

            song_query = db.session.query(Song,Recording,Artist).filter(Recording.id==Song.record_id).\
                filter(Artist.id==Recording.artist_id).\
                filter(Song.song_name.contains(search_string)).group_by(Recording.id)
            results = song_query.all()

        logging.info(f"Search Results={results}")


    else:
        qry = db.session.query(Recording,Artist).filter(Recording.artist_id==Artist.id)
        results = qry.all()

    if not results:
        logging.info(f"No Results Found")
        flash('No results found!',category="warning")
        return redirect('/')
    else:
        # display results

        for _row in results:
            logging.debug(f"{_row.Recording.record_name} {_row.Artist.artist_name}")
        return render_template('show-recordings.html', recordings=results)


@app.route('/show-artist')
def show_artist():
    """
    This function displays the show-artists template to the screen

    :param none:
    :returns: show-artists HTML Template to display the songs
    :raises none
    """
    logging.debug(f"Entering show-artist")
    return render_template('show-artists.html', artists = Artist.query.all() )

@app.route('/show-recording')
def show_recording():
    """
    This function displays the show-recording template to the screen

    :param none:
    :returns: show-recording HTML Template to display the songs
    :raises none
    """
    logging.debug(f"Entering show-recording")
    qry = db.session.query(Recording,Artist).filter(Recording.artist_id==Artist.id)
    results=qry.all()
    return render_template('show-recordings.html', recordings = results )

@app.route('/show-song')
def show_song():
    """
    This function displays the show-song template to the screen

    :param none:
    :returns: show-song HTML Template to display the songs
    :raises none
    """
    logging.debug(f"Entering show-song")
    return render_template('show-songs.html', songs = Song.query.all() )

@app.route('/new_artist', methods=['GET', 'POST'])
def new_artist():
    """
    This function will add a new Artist to the database

    :param none:
    :returns: new_album HTML Template to add the new userl
    :raises none
    """
    logging.debug(f"Entering new_artist")
    form = ArtistForm(request.form)

    if request.method == 'POST' and form.validate():

        exists = Artist.query.filter(Artist.artist_name == form.artist_name.data).first()

        if exists:
            logging.info(f"{form.artist_name.data} already exists in the database!")
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

        flash(message, category=category)

        return redirect('/')

    return render_template('new_artist.html', form=form)

def save_form(form,artistid,new=False):
    """
    This function will save the data when adding a new recording

    :param form: The form object that we defined
    :param artistid: The artist id that we want to add a recording it
    :returns: Boolean value if the insertion was successful
    :raises none
    """
    logging.debug(f"Entering save_form")
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

    # Not Sure this is the best way to get data from the form, but it is the only option that would work

    recording.count_lp = int(form.count_lp.raw_data[0])
    recording.count_45 = int(form.count_45.raw_data[0])
    recording.count_78 = int(form.count_78.raw_data[0])
    recording.count_cassette = int(form.count_cassette.raw_data[0])
    recording.count_copy_cassette = int(form.count_copy_cassette.raw_data[0])
    recording.count_cd = int(form.count_cd.raw_data[0])
    recording.count_copy_cd = int(form.count_copy_cd.raw_data[0])
    recording.count_digital = int(form.count_digital.raw_data[0])

    try:
        db.session.add(recording)

        songs = form.songs.data.splitlines()
        for i in songs:
            temp = Song()
            temp.record_id = recording.id
            temp.song_name = i
            temp.id = generate_uniqueID()
            logging.debug(f"{temp}")
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
    logging.debug(f"Entering new_recording")
    qry = db.session.query(Artist).filter(Artist.id == artistid)
    results = qry.first()
    if results:

        logging.info(f"Adding a new recording for ArtistID: {artistid}, {results.artist_name}")

        form = AlbumForm(request.form)
        form.artist_id.data = artistid
        form.artist_name.data = results.artist_name


        if request.method == 'POST' and form.validate():
            logging.info (f"Saving New Record")
            save_form(form,artistid,True)
            return redirect ('/')

        else:
            form.count_lp.data = 0
            form.count_45.data = 0
            form.count_78.data = 0
            form.count_cassette.data = 0
            form.count_copy_cassette.data = 0
            form.count_cd.data = 0
            form.count_copy_cd.data = 0
            form.count_digital.data = 0

            return render_template('new_album.html', form=form, artistname=results.artist_name)
    else:
        message = "Unable to add recording to Artist ID " + artistid + ". Artist doesn't exist, please add a new artist!"
        category = "danger"
        flash(message, category=category)
        return redirect ('/')

def update_records(album, form):


    logging.debug(f"Entering update_records")

    album.record_name = form.album_name.data
    album.label_number = form.label_number.data
    album.label = form.label.data
    album.type = form.label.data
    album.cover = form.cover.data
    album.word = form.word.data

    album.count_lp = int(form.count_lp.raw_data[0])
    album.count_45 = int(form.count_45.raw_data[0])
    album.count_78 = int(form.count_78.raw_data[0])
    album.count_cassette = int(form.count_cassette.raw_data[0])
    album.count_copy_cassette = int(form.count_copy_cassette.raw_data[0])
    album.count_cd = int(form.count_cd.raw_data[0])
    album.count_copy_cd = int(form.count_copy_cd.raw_data[0])
    album.count_digital = int(form.count_digital.raw_data[0])

    songs_edited = form.songs.data.splitlines()

    song_query = db.session.query(Song).filter(Song.record_id == album.id)
    song_results = song_query.all()

    song_existing = []
    for i in song_results:
        song_existing.append(i.song_name)



    if (songs_edited == song_results):
        logging.debug(f"No Changes with Songs")
    else:
        logging.debug(f"Changes occured with Songs")

        songs_in_orig_not_new = set(song_existing) - set(songs_edited)
        songs_in_new_not_orig = set(songs_edited) - set(song_existing)

        if len(songs_in_new_not_orig) > 0:
            logging.debug(f"We need to add the following: {songs_in_new_not_orig}")
            for i in songs_in_new_not_orig:
                temp = Song()
                temp.record_id = album.id
                temp.song_name = i
                temp.id = generate_uniqueID()
                db.session.add(temp)

        if len(songs_in_orig_not_new) > 0:
            logging.debug(f"We need to delete the following: {songs_in_orig_not_new}")
            for i in songs_in_orig_not_new:
                song_query = db.session.query(Song).filter(Song.record_id == album.id).filter(Song.song_name == i)
                song_results = song_query.delete()




    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        rc = False
    else:
        rc = True

    return rc


@app.route("/view_recording/<recordid>", methods=('GET', 'POST'))
def viewrecordingdetails(recordid):
    """
    This function will create the HTML page to view an existing recording given an recordid ID.

    :param artistid: The ID of the Record
    :returns: album_details HTML Template to add the new user
    :raises none
    """
    logging.debug(f"Entering viewrecordingdetails")

    if request.method == 'POST':
        logging.debug(f"Attempting to Save Changes")
        logging.debug(f"{global_album_storage}")

        qry = db.session.query(Recording).filter(Recording.id == recordid)
        results = qry.first()

        form=AlbumForm(formdata=request.form,obj=results)

        success = update_records(results,form)
        if not success:
            message = "ERROR: " + str(e.__dict__['orig'])
            category = "danger"
        else:
            message = "Successfully Updated Recording: " + results.record_name
            category = "success"

        flash(message, category=category)
        return redirect ('/')
    else:

        qry = db.session.query(Recording).filter(Recording.id == recordid)
        results = qry.first()

        form = AlbumForm()

        #Save the form

        form.album_name.data = results.record_name
        form.label_number.data = results.label_number
        form.label.data = results.label
        form.cover.data = results.cover
        form.word.data = results.word
        form.count_lp.data = results.count_lp
        form.count_45.data = results.count_45
        form.count_78.data = results.count_78
        form.count_cassette.data = results.count_cassette
        form.count_copy_cassette.data = results.count_copy_cassette
        form.count_cd.data = results.count_cd
        form.count_copy_cd.data = results.count_copy_cd
        form.count_digital.data = results.count_digital

        global_album_storage.append((form))

        qry = db.session.query(Artist).filter(Artist.id == results.artist_id)
        results = qry.first()

        song_query = db.session.query(Song).filter( Song.record_id == recordid)
        song_results = song_query.all()

        tracks_display=""
        tracks=[]
        for song in song_results:
            tracks_display += song.song_name+"\n"
            tracks.append(song.song_name)

        form.songs.data = tracks_display
        global_album_storage.append(tracks)
        return render_template('album-details.html', form=form, artistname=results.artist_name)

    return redirect ('/')


@app.route("/setup", methods=('GET', 'POST'))
def setup():
    '''
    This function will display the setup page used for configuring the application.

    :return: the config.html form or if it was a post, then a redirect back to the main screen
    :rtype:
    '''
    logging.debug(f"Entering setup")

    form = SetupForm()

    if request.method == 'POST' and form.validate():

        if request.form.get('debugmode') == 'y':
            logging.info(f"Changing Logging Level to DEBUG")
            logging.getLogger().setLevel(logging.DEBUG)

        else:
            logging.info(f"Changing Logging Level to INFO")
            logging.getLogger().setLevel(logging.INFO)

        return redirect('/')

    else:
        if logging.root.level == logging.INFO:
            form.debugmode.data = False
        else:
            form.debugmode.data = True
        #form.debugmode.data = app.config.get('DEBUGAPP')

    return render_template('config.html',form=form)