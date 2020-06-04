import os
import imdb

db = imdb.IMDb()

movies = db.get_top250_movies()
movies = movies[225:]

wrk_dir = os.getcwd() + "\\Sample Files\\"

for movie in movies:
    mov_title = str(movie).replace(":", " -").replace("?", "")
    mov_title+=".mkv"
    path = wrk_dir + mov_title
    

    f = open(path, 'w')
    f.close()
