##### DB Models #####

class Delegacion(db.Model):
    __tablename__="Delegacion"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return f"{self.name} | {self.gender}"

class Calidad(db.Model):
    __tablename__ = "Calidad"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    neighborhood= db.Column(db.String(64))
    street= db.Column(db.String(64), nullable=False)
    num_samples = db.Column(db.String(10))   #Use datetime here
    readings = db.Column(db.String(5))
    average = db.Column(db.String(64))
    percent_none = db.Column(db.Float)
    percent_low = db.Column(db.Float)
    percent_rule = db.Column(db.Float)
    percent_excess = db.Column(db.Float)
    delegacion_id = db.Column(db.Integer, db.ForeignKey('Delegacion.id'))

    def __repr__(self):
        return f"{self.date} | {self.street} | {self.average}"


############################# Flask Routes ######################################

## Main route
# @app.route('/')
# def index():
#     songs = Song.query.all()
#     num_songs = len(songs)
#     return render_template('index.html', num_songs=num_songs)
#
# @app.route('/song/new/<title>/<artist>/<genre>/')
# def new_song(title, artist, genre):
#     if Song.query.filter_by(title=title).first(): # if there is a song by that title
#         return "That song already exists! Go back to the main app!"
#     else:
#         artist = get_or_create_artist(artist)
#         song = Song(title=title, artist_id=artist.id,genre=genre)
#         session.add(song)
#         session.commit()
#         return "New song: {} by {}. Check out the URL for ALL songs to see the whole list.".format(song.title, artist.name)
#
# @app.route('/all_songs')
# def see_all():
#     all_songs = [] # Will be be tuple list of title, genre
#     songs = Song.query.all()
#     for s in songs:
#         artist = Artist.query.filter_by(id=s.artist_id).first() # get just one artist instance
#         all_songs.append((s.title,artist.name, s.genre)) # get list of songs with info to easily access [not the only way to do this]
#     return render_template('all_songs.html',all_songs=all_songs) # check out template to see what it's doing with what we're sending!
#
# @app.route('/all_artists')
# def see_all_artists():
#     artists = Artist.query.all()
#     names = []
#     for a in artists:
#         num_songs = len(Song.query.filter_by(artist_id=a.id).all())
#         newtup = (a.name,num_songs)
#         names.append(newtup) # names will be a list of tuples
#     return render_template('all_artists.html',artist_names=names)
#
# @app.route('/songs/<genre>/')
# def by_genre(genre):
#     songs = Song.query.filter_by(genre=genre)
#     to_display = []
#     for s in songs:
#         artist = Artist.query.filter_by(id=s.artist_id).first() # get just one artist instance
#         to_display.append((s.title,artist.name, s.genre)) # get list of songs with info to easily access [not the only way to do this]
#     return render_template('genre_songs.html',all_songs=to_display, gen=genre)
#
#
if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
