from imdb import IMDb
import csv
from get_functions import *

ia = IMDb()

movie_titles = ['the matrix', 'terminator', 'crocodile dundee', 'frozen ii'] #write names of movies here to be searched

noMovies = len(movie_titles)
movies = []
movieTitle = []
movieYear = []
movieDuration = []
movieRating = []
movieGenre = []
movieDirectors = []
movieStarRating = []

with open ('movieDB.csv') as csv_file :
    csv_write = csv.writer(csv_file, delimiter = ',')

for x in range(noMovies):
    temp = movie_titles[x]
    search = ia.search_movie(temp)
    movies.append(search[0])
    
    
    

print(movies)

print(movieTitle)    

