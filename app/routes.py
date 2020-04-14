from flask import render_template, request, flash, redirect
from musicdb import app
from app import db
from app.models import Artist, Recording, Song
from app.forms import MusicSearchForm, AlbumForm, ArtistForm, SetupForm, GenericSearchForm
import wtforms
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from app.utils import generate_uniqueID,cleanup_songs
#from app import musicdb_config
#from app import version
from orderedset import OrderedSet
import time
import logging
from app.appconfig import AppConfig
from logging.handlers import RotatingFileHandler

# Global Data to Persist Between Function Calls
global_album_storage = []
# Create a global application configuration object
musicdb_config = AppConfig()
# Set the Version Number
version = ".9b"

@app.before_first_request
def appinit():

    logging.getLogger()
    handler = RotatingFileHandler("musicdb.log", maxBytes=1000000, backupCount=5)
    logging.basicConfig(level=logging.INFO, format='%(asctime)-15s-%(funcName)-15s %(levelname)-8s %(message)s', \
                        handlers=[handler, logging.StreamHandler()])
    if musicdb_config.getitem("LOGGING") == 'DEBUG':
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def main():
    """
    This function will create the HTML page to render the home page

    :param
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


@app.route('/about')
def about():
    """
    This route point displays the about screen to print the version and copyright of the software.

    :return: about.html template which represents the about screen.
    :rtype:
    """
    logging.debug(f"Entering about")
    return render_template("about.html",version=version)

@app.route('/search',methods=['GET', 'POST'])
def search():
    """
    This route point displays the generic search form to display the generic query screen.

    :return: If the method was a GET, then we return the search.html form.   If the method was a post
             then we return the output of the search results.
    :rtype:
    """

    logging.debug(f"Entering search")

    search = GenericSearchForm(request.form)

    if request.method == 'POST':
        logging.debug("POST was pressed")
        return generic_search(search)

    return render_template("search.html", form=search)


def generic_search(search):
    """

    :param search: This is the data representing the form Search
    :type search: GenericSearchForm
    :return: The show-recordings.html template with the appropriate day populated.
    :rtype:
    """
    logging.debug(f"Entering generic_search")
    results = []
    logging.debug(search.select)


    if search.data['select'] == '45Recordings':
        logging.info(f"Doing a search on 45 Recordings")

        qry = db.session.query(Recording, Artist).filter(Recording.artist_id == Artist.id). \
            filter(Recording.count_45 > 0)
        results = qry.all()
    elif search.data['select'] == '78Recordings':
        logging.info(f"Doing a search on 78 Recordings")

        qry = db.session.query(Recording, Artist).filter(Recording.artist_id == Artist.id). \
            filter(Recording.count_78 > 0)
        results = qry.all()

    elif search.data['select'] == 'DuplicateLPs':
        logging.info(f"Doing a search on Duplicate Lps")

        qry = db.session.query(Recording, Artist).filter(Recording.artist_id == Artist.id). \
            filter(Recording.count_lp > 1)
        results = qry.all()

    elif search.data['select'] == 'RecordingsWithNoCopies':
        logging.info(f"Doing a search on Recording with 0 copies")

        qry = db.session.query(Recording, Artist).filter(Recording.artist_id == Artist.id). \
            filter(and_(Recording.count_lp == 0,Recording.count_45 == 0, Recording.count_78 == 0, \
                   Recording.count_cd == 0, Recording.count_cassette == 0, Recording.count_copy_cassette == 0, \
                   Recording.count_copy_cd == 0,Recording.count_digital == 0))
        results = qry.all()

    elif search.data['select'] == 'RecordingsNotDigital':
        logging.info(f"Doing a search on Recordings without a digital copy")

        qry = db.session.query(Recording, Artist).filter(Recording.artist_id == Artist.id). \
            filter(Recording.count_digital == 0)
        results = qry.all()

    logging.info(f"Search Results={results}")


    return render_template('show-recordings.html', recordings=results)

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

            qry = db.session.query(Recording, Artist).filter(Recording.artist_id == Artist.id). \
                filter(Artist.artist_name.contains(search_string))
            results = qry.all()


        elif search.data['select'] == 'Album':
            logging.info(f"Doing a search on Album='{search_string}'")
            qry = db.session.query(Recording, Artist).filter(Recording.artist_id == Artist.id). \
                filter(Recording.record_name.contains(search_string))
            results = qry.all()

        elif search.data['select'] == 'Song':
            logging.info(f"Doing a search on Song='{search_string}'")

            song_query = db.session.query(Song, Recording, Artist).filter(Recording.id == Song.record_id). \
                filter(Artist.id == Recording.artist_id). \
                filter(Song.song_name.contains(search_string)).group_by(Recording.id)
            results = song_query.all()
        elif search.data['select'] == 'ArtistOnly':
            logging.info(f"Doing an Artist Search on Artist='{search_string}'")

            artist_query = db.session.query(Artist).filter(Artist.artist_name.contains(search_string)). \
                group_by(Artist.id)
            results = artist_query.all()

        logging.info(f"Search Results={results}")


    else:
        qry = db.session.query(Recording, Artist).filter(Recording.artist_id == Artist.id)
        results = qry.all()

    if not results:
        logging.info(f"No Results Found for '{search_string}'")
        flash(f'No results found for {search_string}', category="warning")
        return redirect('/')
    else:
        # display results

        if search.data['select'] == 'ArtistOnly':
            for _row in results:
                logging.debug(f"{_row.artist_name}")
            return render_template('show-artists.html', artists=results)

        else:
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
    return render_template('show-artists.html', artists=Artist.query.all())


@app.route('/show-recording')
def show_recording():
    """
    This function displays the show-recording template to the screen

    :param none:
    :returns: show-recording HTML Template to display the songs
    :raises none
    """
    logging.debug(f"Entering show-recording")
    qry = db.session.query(Recording, Artist).filter(Recording.artist_id == Artist.id)
    results = qry.all()
    return render_template('show-recordings.html', recordings=results)


@app.route('/show-song')
def show_song():
    """
    This function displays the show-song template to the screen

    :param none:
    :returns: show-song HTML Template to display the songs
    :raises none
    """
    logging.debug(f"Entering show-song")
    return render_template('show-songs.html', songs=Song.query.all())


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

    artist_name_cleaned = form.artist_name.data.strip().title()

    if request.method == 'POST' and form.validate():

        exists = Artist.query.filter(Artist.artist_name == artist_name_cleaned).first()

        if exists:
            logging.info(f"{artist_name_cleaned} already exists in the database!")
            message = f"{artist_name_cleaned} already exists in the database!"
            category = "danger"
        else:

            new_artist = Artist()
            new_artist.artist_name = artist_name_cleaned
            ts = int(time.time())
            new_artist.id = ts

            try:
                db.session.add(new_artist)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                message = "ERROR: " + str(e.__dict__['orig'])
                category = "danger"
            else:
                message = "Successfully Added Artist: " + new_artist.artist_name + ", with ID: " + str(new_artist.id)
                category = "success"

        flash(message, category=category)

        return redirect('/')

    return render_template('new_artist.html', form=form)


def save_form(form, artistid, new=False):
    """
    This function will save the data when adding a new recording

    :return:
    :rtype:
    :param new:
    :type new:
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
    recording.record_name = form.album_name.data.strip().title()
    recording.label_number = form.label_number.data.strip().title()
    recording.label = form.label.data.strip()
    recording.type = form.label.data.strip().title()
    recording.cover = form.cover.data
    recording.word = form.word.data

    # Determine if the recording name is blank or spaces, then don't save
    if recording.record_name.isspace() or recording.record_name is "":
        logging.info(f"Unable to add record since name is not blank.")
        message = "Unable to add recording since name is not blank."
        category = "danger"
        rc = False

        flash(message, category=category)

        return rc

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

        # Split the song names
        songs = cleanup_songs(form.songs.data.splitlines())
        for i in songs:
            # Create a temporary song object to hold the album ID
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

    return rc


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
            logging.info(f"Saving New Record")
            save_form(form, artistid, True)
            return redirect('/')

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
        return redirect('/')


def update_records(album, form):
    logging.debug(f"Entering update_records")

    album.record_name = form.album_name.data.strip().title()
    album.label_number = form.label_number.data.strip().title()
    album.label = form.label.data.strip()
    album.type = form.label.data
    album.cover = form.cover.data
    album.word = form.word.data

    compare = lambda x : int(x) if x.isdigit() else 0

    album.count_lp = compare(form.count_lp.raw_data[0])
    album.count_45 = compare(form.count_45.raw_data[0])
    album.count_78 = compare(form.count_78.raw_data[0])
    album.count_cassette = compare(form.count_cassette.raw_data[0])
    album.count_copy_cassette = compare(form.count_copy_cassette.raw_data[0])
    album.count_cd = compare(form.count_cd.raw_data[0])
    album.count_copy_cd = compare(form.count_copy_cd.raw_data[0])
    album.count_digital = compare(form.count_digital.raw_data[0])

    songs_edited = cleanup_songs(form.songs.data.splitlines())

#    print (songs_edited)
#    #TODO: REMOVE ANY OF THE BLANK LINES
#    blanks=[]
#    count=0
#    for i in songs_edited:
#        if i.isspace() or i is "":
#            blanks.append(i)
#        count += 1
#
#    print (blanks)

#    for i in blanks:
#        songs_edited.remove(i)
#    print(songs_edited)

#    final_songs=[]
#    for i in songs_edited:
#        final_songs.append(i.strip())

#    print (final_songs)



    song_query = db.session.query(Song).filter(Song.record_id == album.id)
    song_results = song_query.all()

    song_existing = []
    for i in song_results:
        song_existing.append(i.song_name)

    if (songs_edited == song_results):
        logging.debug(f"No Changes with Songs")
    else:
        logging.debug(f"Changes occured with Songs")

#        songs_in_orig_not_new = set(song_existing) - set(songs_edited)
#        songs_in_new_not_orig = set(songs_edited) - set(song_existing)
        songs_in_orig_not_new = OrderedSet(song_existing) - OrderedSet(songs_edited)
        songs_in_new_not_orig = OrderedSet(songs_edited) - OrderedSet(song_existing)

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
        return False, e
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
        # Let's check to see if the Cancel button was pressed, if so, cancel the update
        if 'Cancel' in request.form :
            logging.info(f"Cancelling the updating of a recording with id {recordid}")
            message = "Canceled Updating Recording: "
            category = "warning"
            flash(message, category=category)
            return redirect('/')
        logging.debug(f"Attempting to Save Changes")

        qry = db.session.query(Recording).filter(Recording.id == recordid)
        results = qry.first()

        form = AlbumForm(formdata=request.form, obj=results)

        success = update_records(results, form)

        if not success:
            message = f"ERROR: Unable to update the recording {recordid}"
            category = "danger"
        else:
            message = f"Successfully Updated Recording: {results.record_name}"
            category = "success"

        flash(message, category=category)
        return redirect('/')
    else:

        qry = db.session.query(Recording).filter(Recording.id == recordid)
        results = qry.first()

        form = AlbumForm()

        # Save the form

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

        global_album_storage.append(form)

        qry = db.session.query(Artist).filter(Artist.id == results.artist_id)
        results = qry.first()

        song_query = db.session.query(Song).filter(Song.record_id == recordid)
        song_results = song_query.all()

        tracks_display = ""
        tracks = []
        for song in song_results:
            tracks_display += song.song_name + "\n"
            tracks.append(song.song_name)

        form.songs.data = tracks_display
        global_album_storage.append(tracks)
        return render_template('album-details.html', form=form, artistname=results.artist_name)

    return redirect('/')


@app.route("/setup", methods=('GET', 'POST'))
def setup():
    """
    This function will display the setup page used for configuring the application.

    :return: the config.html form or if it was a post, then a redirect back to the main screen
    :rtype:
    """
    logging.debug(f"Entering setup")

    form = SetupForm()

    if request.method == 'POST' and form.validate():

        if request.form.get('debugmode') == 'y':
            logging.info(f"Changing Logging Level to DEBUG")
            logging.getLogger().setLevel(logging.DEBUG)
            musicdb_config.setitem("LOGGING", "DEBUG")

        else:
            logging.info(f"Changing Logging Level to INFO")
            logging.getLogger().setLevel(logging.INFO)
            musicdb_config.setitem("LOGGING", "INFO")

        return redirect('/')

    else:
        if logging.root.level == logging.INFO:
            form.debugmode.data = False
        else:
            form.debugmode.data = True

    return render_template('config.html', form=form)


@app.route("/integritycheck", methods=(['GET']))
def integritycheck():
    """
    This function does a very simple integrity check for the database.
    :return: redirect back to the main screen
    :rtype:
    """

# Query to determine if Artist exists without an album:
# select count(artist.artist_name) from artist left join recording ON recording.artist_id = artist.id where recording.artist_id IS NULL

#Query to determine which Songs exist without an album:
#select count(song.song_name) from song left join recording ON recording.id = song.id where recording.id IS NULL



    qry = db.session.query(Recording.record_name).outerjoin(Artist).filter()
    number = qry.count()

    print (f"{number}")

    return redirect('/')