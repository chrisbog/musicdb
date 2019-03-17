from flask import render_template, request, flash, redirect
from musicdb import app
from app import db
from app.models import Artist,Recording,Song
from app.forms import MusicSearchForm

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
        flash('No results found!')
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