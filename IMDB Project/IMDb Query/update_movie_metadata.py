import os
import PySimpleGUI as sg

from get_tmdb_data import make_tmdb_call
from get_movie_metadata import get_track_info
from mkv_prop_edit import *

mp_s = 'mkvpropedit'
video_fns = {

    'codec_id': e_codec_id,
    'commercial_name': e_codec_name,
    'sampled_width': e_d_width,
    'sampled_height': e_d_height

}
audio_fns = {

    'codec_id': e_codec_id,
    'commercial_name': e_codec_name,
    'language': e_language,
    'channel_s': e_channels,
    'sampling_rate': e_sampling_rate,
    'bit_depth': e_bit_depth

}
subtitle_fns = {

    'codec_id': e_codec_id,
    'commercial_name': e_codec_name,
    'language': e_language

}


def start_update(path, movie, main_window):
    print("getting movie info")
    movie_info = make_tmdb_call(movie)
    print("getting track info")
    track_info = get_track_info(path, movie)

    if movie_info:
        prop_cmd = f'{mp_s} \"{path}\\{movie}\" --set \"title={movie_info.get("title")}\" '
    else:
        prop_cmd = f'{mp_s} \"{path}\\{movie}\" '
        main_window.write_event_value('-TMDBERR-', movie)

    try:
        # video tracks
        for track, info in enumerate(track_info[0]):
            video_to_do = [func for func in video_fns if func in info]
            prop_cmd += e_video_track(track + 1)

            for item in video_to_do:
                prop_cmd += video_fns[item](info[item])

        # audio tracks
        for track, info in enumerate(track_info[1]):
            audio_to_do = [func for func in audio_fns if func in info]
            prop_cmd += e_audio_track(track + 1)

            for item in audio_to_do:
                prop_cmd += audio_fns[item](info[item])

        # subtitle tracks
        for track, info in enumerate(track_info[2]):
            subtitle_to_do = [func for func in subtitle_fns if func in info]
            prop_cmd += e_sub_track(track + 1)

            for item in subtitle_to_do:
                prop_cmd += subtitle_fns[item](info[item])

        # print(prop_cmd)
        subprocess.run(prop_cmd)

        # print("Finish prop cmd\n\nDone!!")

        print("Starting file edit for movie: ", movie)

        if (movie.find("tmdb") == -1) and movie_info:
            src = f"{path}\\{movie}"
            new_name = movie.split('.')
            new_name = new_name[0] + " [tmdbid=" + str(movie_info['id']) + "]" + "." + new_name[1]
            dst = f"{path}\\{new_name}"

            os.rename(src, dst)

    except BaseException as err:
        print(f"Error while performing update: {err=}, {type(err)=}")
    # result = subprocess.run(prop_cmd, capture_output=True)
    # print(result.stdout)


def folder_update(directory, main_window):
    movie_count = 0
    for root, dirs, files in os.walk(directory):
        for movie in files:
            if '.mkv' in movie:
                movie_count += 1

    main_window.write_event_value('-MOVCOUNT-', movie_count)
    movie_prog = 0

    for root, dirs, files in os.walk(directory):
        for movie in files:
            if '.mkv' in movie:
                movie_prog += 1
                start_update(root, movie, main_window)
                #print(root, movie, make_tmdb_call(movie))
                main_window.write_event_value('-MOVEPROG-', movie_prog)


if __name__ == '__main__':
    start_update('O:\\Movies', 'Iron Man 2 (2010) 2.mkv')
