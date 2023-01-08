import requests as r
import json

from get_movie_details_from_file import file_movie_name as mov_name
from get_movie_details_from_file import file_movie_year as mov_year

genre_dictionary = {

    12: "Adventure",
    14: "Fantasy",
    16: "Animation",
    18: "Drama",
    27: "Horror",
    28: "Action",
    35: "Comedy",
    36: "History",
    37: "Western",
    53: "Thriller",
    80: "Crime",
    99: "Documentary",
    878: "Science Fiction",
    9648: "Mystery",
    10402: "Music",
    10749: "Romance",
    10752: "War",
    10751: "Family",
    10770: "TV Movie"

}


def make_tmdb_call(movie_file):
    """
    Given a string
    :param movie_file:

    The program will return
    :return:

    A dict type containing the valuable movie information.
    """
    name = mov_name(movie_file)
    year = mov_year(movie_file)

    name = name.strip().replace(" ", "%20").replace(".mkv", "").replace(",", "%2C")

    if year:
        tmdb_call_string = f'https://api.themoviedb.org/3/search/movie?api_key=629b1dbf49450758fdd0904c55158104&' \
                           f'language=en-US&query={name}&page=1&include_adult=false&year={year}'
    else:
        tmdb_call_string = f'https://api.themoviedb.org/3/search/movie?api_key=629b1dbf49450758fdd0904c55158104&' \
                           f'language=en-US&query={name}&page=1&include_adult=false'

    # print("movie info:", name, year)

    tmdb_response = r.get(tmdb_call_string)
    movie_info = json.loads(tmdb_response.text)

    if not movie_info["results"]:
        tmdb_call_string = f'https://api.themoviedb.org/3/search/movie?api_key=629b1dbf49450758fdd0904c55158104&' \
                           f'language=en-US&query={name}&page=1&include_adult=false'
        tmdb_response = r.get(tmdb_call_string)
        movie_info = json.loads(tmdb_response.text)

    if not movie_info["results"]:
        return None

    info_list = movie_info["results"][0]

    mov_id = info_list["id"]

    tmdb_id_req = 'https://api.themoviedb.org/3/movie/' + str(mov_id) + '?api_key=629b1dbf49450758fdd0904c55158104' \
                                                                        '&language=en-US'
    precise_movie = r.get(tmdb_id_req)
    precise_info = json.loads(precise_movie.text)

    # for key in precise_info:
    #    print(key)
    # print(precise_info)

    collection = is_part_of_collection(precise_info)

    info_to_return = {

        "id": mov_id,
        "plot": precise_info["overview"],
        "genres": compile_genres(info_list["genre_ids"]),
        "tagline": precise_info["tagline"],
        "runtime": precise_info["runtime"],
        "title": precise_info["title"]

    }

    if not collection:
        info_to_return.update({"collection": "None"})
    else:
        info_to_return.update({"collection": collection})

    # print(info_to_return)
    return info_to_return


def compile_genres(genre_list):
    """
    Pass in the info_list["genre_ids"] and this function will return a list of genres in text form.
    :param genre_list:
    :return:
    """

    global genre_dictionary

    genres = []

    for ids in genre_list:
        genres.append(genre_dictionary[ids])

    return genres


def is_part_of_collection(movie_json):
    """
    Given a movie id, this function returns a False boolean if it does not belong to any collection,
    and returns a list with the collection id and name if it does.
    :param movie_json:
    :return:
    """

    collection_info = []

    if type(movie_json["belongs_to_collection"]) == type(None):
        return False
    else:
        collection_info.append(movie_json["belongs_to_collection"]["id"])
        collection_info.append(movie_json["belongs_to_collection"]["name"])

        return collection_info


if __name__ == '__main__':
    # make_call('Star Wars: Episode II - Attack of the Clones (2002) [tmdbid=38319].mkv')
    print(make_tmdb_call('Parker (2013).mkv'))
