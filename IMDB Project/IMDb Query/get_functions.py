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

    movie_data.append(str(tmp_movie)) #Title
    movie_data.append(tmp_movie['year']) #Release Year
    movie_data.append(str(tmp_movie['runtimes'][0] + " minutes")) #Runtime
    first_director = tmp_movie['directors'][0]
    first_director = first_director['name']
    movie_data.append(first_director) #Director
    movie_data.append(tmp_movie['rating']) #Star Rating
    movie_data.append(tmp_movie.get('mpaa')) #MPAA Rating
    cast = []
    for actor in tmp_movie['cast']:
        cast.append(actor['name'])
    movie_data.append(cast) #Cast
    movie_data.append(tmp_movie['plot'][0].split('::')[0]) #Plot
    movie_data.append(tmp_movie['genre']) #Genre
    return movie_data
    
    print('wip')

if __name__ == '__main__':
    print('why run this modle alone?')
    print(get_genre('the matrix'))
