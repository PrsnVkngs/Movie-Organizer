from imdb import IMDb

db = IMDb()

def get_full_infoset():
    return db.get_movie_infoset()

def get_movie(movie):
    movie_name = db.search_movie(movie)[0]
    movie = movie_name.movieID
    movie = db.get_movie(movie)
    return movie

def get_genre(movie):  #using the str() function on a movie variable will return just the name
    tmp = get_movie(movie)
    genre = tmp.get('genre')[0]
    return genre

def get_all_data(movie):
    movie_data = []
    tmp_movie = get_movie(movie)

    movie_name = str(tmp_movie)
    movie_data.append(movie_name)

    
    print('wip')

if __name__ == '__main__':
    print('why run this modle alone?')
    print(get_genre('the matrix'))
