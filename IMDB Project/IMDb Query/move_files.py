import os
import shutil
from pymediainfo import MediaInfo
import gc

from get_functions import *

def detect_directory(directory, desired):
    contents = os.listdir(directory)
    is_present = False
    for each in contents:
        if(each == desired):
            is_present = True
            break
    return is_present

def is_4k ( movie ):
    file_info = MediaInfo.parse ( movie )
    for track in file_info.tracks:
        if track.track_type == 'Video':
            if ( track.width == 3840 ):
                print(str(movie) + "Movie is 4k")
                return True
            else:
                print(str(movie) + "Movie is not 4k")
                return False
            

def move_movie ( movie, path, destination ):
    movie_genre = get_genre ( movie )
    print(movie_genre)
    if detect_directory ( destination, movie_genre ): #detect if there is a directory for the genre.
        if is_4k( path ): #if yes, is the movie 4k?
            if detect_directory ( str ( destination + "\\" + movie_genre ), "4k" ): #if the movie is 4k, is there a 4k directory in the destination?
                shutil.move( path, (destination + "\\" + movie_genre + "\\4k") )
            else:
                os.mkdir ( (destination + "\\" + movie_genre + "\\4k") ) #if no, make one and move it.
                shutil.move( path, (destination + "\\" + movie_genre + "\\4k") )
        else:
            shutil.move( path, (destination + "\\" + movie_genre) )
    
    else: #if no directory for genre, make one and move the movie.
        movie_genre = get_genre ( movie )
        os.mkdir( destination + "\\" + movie_genre )
        if is_4k( path ): #if yes, is the movie 4k?
            if detect_directory ( str ( destination + "\\" + movie_genre ), "4k" ): #if the movie is 4k, is there a 4k directory in the destination?
                shutil.move( path, (destination + "\\" + movie_genre + "\\4k") )
            else:
                os.mkdir ( (destination + "\\" + movie_genre + "\\4k") ) #if no, make one and move it.
                shutil.move( path, (destination + "\\" + movie_genre + "\\4k") )
        else:
            shutil.move( path, (destination + "\\" + movie_genre) )
    gc.collect()   

def move_folder( source, destination ):
    shutil.move( source  , destination )


def walk_directory(directory, destination):

    for root, dirs, files in os.walk(directory):
        for folder in dirs:
            move_folder ( directory + "\\" +folder, destination )
            print( "Moved the folder " + folder + " to the destination" )
        for movie in files:
            print(movie)
            move_movie( movie, directory + "\\" + movie, destination )
            print( "Moved the movie " + movie + " to the destination" )

