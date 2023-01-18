import gc
from pathlib import Path

from get_movie_metadata import get_track_info
from get_tmdb_data import make_tmdb_call
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


def start_update(movie, main_window):

    print("Currently editing the movie: ", movie.name, " in directory: ", movie.parent)



    # print("getting movie info")
    movie_info = make_tmdb_call(movie.name)
    # print("getting track info")
    track_info = get_track_info(movie)

    if movie_info:
        prop_cmd = f'{mp_s} \"{movie.absolute()}\" --set \"title={movie_info.get("title")}\" '
    else:
        prop_cmd = f'{mp_s} \"{movie.absolute()}\" '
        main_window.write_event_value('-TMDBERR-', "Could not retrieve the name for: " + str(movie.name))

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
        result = subprocess.run(prop_cmd, capture_output=True)

        match result.returncode:
            case 0:
                process_result = "Edit successful."
            case 2:
                process_result = "Edit unsuccessful, file likely isn't an mkv."
            case default:
                process_result = "Unknown process code, likely that an error was thrown."

        print("MKV Prop Edit Result: ", process_result)

        # print("Finish prop cmd\n\nDone!!")
        # print("Starting file edit for movie: ", movie)

        if (movie.name.find("tmdb") == -1) and movie_info:
            src = Path(movie)
            new_name = movie.name.split('.')
            new_name = new_name[0] + " [tmdbid=" + str(movie_info['id']) + "]" + "." + new_name[1]
            dst = src.parent / new_name

            src.rename(dst)

    except BaseException as err:
        print(f"Error while performing update: {err=}, {type(err)=}")
        main_window.write_event_value(key='-GENERAL_ERROR-', value=["Check if MKVToolNix and MediaInfo Installation "
                                                                    "Locations are on the system environment "
                                                                    "variable.", "black on yellow"])
    # result = subprocess.run(prop_cmd, capture_output=True)
    # print(result.stdout)


def folder_update(raw_dir, main_window):

    directory = Path(raw_dir)

    movies_to_update = directory.rglob("*.mkv")

    movie_count = 0
    path_list = []

    for m in movies_to_update:
        movie_count += 1
        path_list.append(m)

    main_window.write_event_value('-MOVCOUNT-', movie_count)
    movie_prog = 0

    for movies in path_list:
        start_update(movies, main_window)
        movie_prog += 1
        main_window.write_event_value('-MOVEPROG-', movie_prog)
