#this program is intended to generate empty files -
#with the name of a popular movie in order to test -
#the sorting algorithm. 

import os
import imdb

db = imdb.IMDb()

movies = db.get_top250_movies()


wrk_dir = "O:\\Dummy Movies\\Source\\"

for movie in movies:
    mov_title = str(movie).replace(":", " -").replace("?", "")
    mov_title+=".mkv"
    path = wrk_dir + mov_title

    f = open(path, 'w')
    f.close()
