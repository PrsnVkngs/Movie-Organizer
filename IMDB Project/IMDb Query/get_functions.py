import imdb
import gc

db = imdb.Cinemagoer()


def get_full_infoset():
    return db.get_movie_infoset()


def get_movie(movie):
    results = db.search_movie(movie)

    if '(' in movie:
        movie_year = int(movie[-5:-1])  # Gets the movie name by substringing it from the file name.
        found_movie = False  # boolean that knows whether the function has found a match for the movie.
        for movie_r in results:  # go through each movie result and check if the movie year matches.
            try:
                if movie_r['year'] == movie_year:
                    movie_name = movie_r
                    found_movie = True  # when the matching year is found, set the movie variable and break.
                    break
            except KeyError:
                continue

        if found_movie:
            print("Found movie " + movie_name['title'] + " in IMDb.")
        else:
            print("Did not find any results for " + movie + ". Selecting the first option.")
            movie_name = results[0]
    else:
        movie_name = results[0]

    movie = movie_name.movieID
    movie = db.get_movie(movie)
    gc.collect()
    return movie


def get_genre(movie):  # using the str() function on a movie variable will return just the name
    tmp = get_movie(movie[:-4])
    try:
        genres = tmp.get('genre')  # get list of genres from IMDB
        gc.collect()
        if 'Action' in genres:
            return 'Action Adventure'
        elif 'Adventure' in genres:
            return 'Action Adventure'
        elif 'War' in genres:
            return 'War'
        else:
            return genres[0]
    except:
        return "None"


def get_star_rating(movie):
    temp = get_movie(movie[:-4])
    try:
        m_rating = temp['rating']
    except:
        m_rating = 0
    gc.collect()
    return m_rating


def get_all_data(movie):
    movie_data = []
    tmp_movie = get_movie(movie)

    movie_data.append(str(tmp_movie))  # Title
    movie_data.append(tmp_movie['year'])  # Release Year
    movie_data.append(str(tmp_movie['runtimes'][0] + " minutes"))  # Runtime
    first_director = tmp_movie['directors'][0]
    first_director = first_director['name']
    movie_data.append(first_director)  # Director
    movie_data.append(tmp_movie['rating'])  # Star Rating
    movie_data.append(tmp_movie.get('mpaa'))  # MPAA Rating
    cast = []
    # for actor in tmp_movie['cast']:
    #    cast.append(actor['name'])
    # movie_data.append(cast) #Cast
    # movie_data.append(tmp_movie['plot'][0].split('::')[0]) #Plot
    movie_data.append(tmp_movie['genre'])  # Genre
    return movie_data

    print('wip')


if __name__ == '__main__':
    print('why run this module alone?')
    print(get_genre('the matrix'))
