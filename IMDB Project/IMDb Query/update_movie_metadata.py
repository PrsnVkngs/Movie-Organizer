from _winapi import CREATE_NO_WINDOW
from pathlib import Path
import logging
from json import JSONDecodeError
from tempfile import NamedTemporaryFile

from get_movie_details_from_file import has_tmdb_tag
from get_movie_metadata import get_track_info
from get_tmdb_data import make_tmdb_call
from mkv_prop_edit import *
from xml_builder import MatroskaTagger

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


def process_tracks(track_info, track_type, edit_track_fn, track_fns):
    cmd = ""
    for track, info in enumerate(track_info):
        to_do = [func for func in track_fns if func in info]
        cmd += edit_track_fn(track + 1)
        for item in to_do:
            cmd += track_fns[item](info[item])
    return cmd


def start_update(movie, main_window, settings):
    print("Currently editing the movie: ", movie.name, " in directory: ", movie.parent)

    if has_tmdb_tag(movie.name) and not settings['update-force']:  # update force setting
        if settings['verbose']:
            main_window.write_event_value(key='-GENERAL_ERROR-',
                                          value=[f"The movie: {movie.name} has a TMDB tag and does not need updating.",
                                                 "black on green"])
        print('\n')
        return None

    # print("getting movie info")
    try:
        movie_info = make_tmdb_call(movie.name)
    except JSONDecodeError:
        main_window.write_event_value(key='-GENERAL_ERROR-',
                                      value=[f"Error retrieving movie info for the movie: {movie.name}"
                                             f" from TMDB.", "black on red"])
        return
    # print("getting track info")
    track_info, xml_info = get_track_info(movie)

    if movie_info:
        prop_cmd = f'{mp_s} \"{movie.absolute()}\" --set \"title={movie_info.get("title")}\" '
    else:
        prop_cmd = f'{mp_s} \"{movie.absolute()}\" '
        if settings[0]:
            main_window.write_event_value('-TMDBERR-', "Could not retrieve the name for: " + str(movie.name))

    # print("constructing mkv prop edit command.")
    for track in track_info.values():
        if track != 0:
            for num, info in enumerate(track):
                t_type = info.pop('track-type')
                t_type = t_type[0].lower()
                prop_cmd += f"--edit track:{t_type}{num + 1} "
                for detail, value in info.items():
                    prop_cmd += f"--set {detail}=\"{value}\" "

    # print(prop_cmd)
    result = 3
    try:
        result = subprocess.run(prop_cmd, capture_output=True, creationflags=CREATE_NO_WINDOW)
    except FileNotFoundError as err:
        if settings['verbose']:
            print(f"Error while performing update: {err=}, {type(err)=}")
            main_window.write_event_value(key='-GENERAL_ERROR-',
                                          value=["Check if MKVToolNix and MediaInfo Installation"
                                                 "Locations are on the system environment "
                                                 "variable.", "black on yellow"])
        return
    except BaseException as err:
        if settings['verbose']:
            print(f"Error while editing the metadata: {err=}, {type(err)=}")
            main_window.write_event_value(key='-GENERAL_ERROR-',
                                          value=["Generic error occurred while editing metadata.", "black on yellow"])
        return

    match result.returncode:
        case 0:
            process_result = "Edit successful."
        case 1:
            process_result = "A minor error occurred but edits successful."
        case 2:
            process_result = "Edit unsuccessful, major error occurred."
        case default:
            process_result = "Unknown process code, likely that an error was thrown."

    if settings['verbose']:
        print("Movie base info edit result: ", process_result)

    # Start the tag additions here:
    with NamedTemporaryFile(mode='w+', delete=False, suffix='.xml') as video, NamedTemporaryFile(mode='w+', delete=False, suffix='.xml') as audio:
        # create the matroska tagger classes
        video_xml = MatroskaTagger(track_uid=xml_info['Video'].pop('trackuid'))
        audio_xml = MatroskaTagger(track_uid=xml_info['Audio'].pop('trackuid'))

        # populate the matroska taggers with the info.
        video_xml.parse_dict(xml_info['Video'])
        audio_xml.parse_dict(xml_info['Audio'])

        # write their contents to the file
        video.write(video_xml.get_xml_string())
        video.flush()
        audio.write(audio_xml.get_xml_string())
        audio.flush()

        tag_comm = f'{mp_s} \"{movie.absolute()}\" --tags track:v1:\"{video.name}\" --tags track:a1:\"{audio.name}\"'
        # print(tag_comm)

        try:
            tag_result = subprocess.run(tag_comm, capture_output=True, creationflags=CREATE_NO_WINDOW)

            match tag_result.returncode:
                case 0:
                    process_result = "Edit successful."
                case 1:
                    process_result = "A minor error occurred but edits successful."
                case 2:
                    process_result = f"Edit unsuccessful, major error occurred. Additional info {tag_result.stdout}"
                case default:
                    process_result = "Unknown process code, likely that an error was thrown."

            print("Additional tags addition result: ", process_result)

        except FileNotFoundError as err:
            if settings['verbose']:
                print(f"Error while performing update: {err=}, {type(err)=}")
                main_window.write_event_value(key='-GENERAL_ERROR-',
                                              value=["Check if MKVToolNix and MediaInfo Installation"
                                                     "Locations are on the system environment "
                                                     "variable.", "black on yellow"])
            return

    # end the edits using the temp files

    # TODO compute the tags based on user setting:
    if settings['stats']:
        compute_cmd = f'{mp_s} \"{movie.absolute()}\" --add-track-statistics-tags'

        stats_result = subprocess.run(compute_cmd, capture_output=True, creationflags=CREATE_NO_WINDOW)

        match stats_result.returncode:
            case 0:
                process_result = "Computation successful."
            case 1:
                process_result = "A minor error occurred but stats written to file."
            case 2:
                process_result = f"Write to file unsuccessful, major error occurred. Additional details: {stats_result.stdout}"
            case default:
                process_result = "Unknown process code, likely that an error was thrown."

        print("Additional stats computation result: ", process_result)

    # print("Finish prop cmd\n\nDone!!")
    # print("Starting file edit for movie: ", movie)

    if (movie.name.find("tmdb") == -1) and movie_info:
        src = Path(movie)
        new_name = movie.name.split('.')
        new_name = new_name[0] + " [tmdbid=" + str(movie_info['id']) + "]" + "." + new_name[1]
        dst = src.parent / new_name

        src.rename(dst)

    print('\n')

    # result = subprocess.run(prop_cmd, capture_output=True)
    # print(result.stdout)


def folder_update(raw_dir, main_window, settings):
    directory = Path(raw_dir)

    movies_to_update = directory.rglob("*.mkv")

    movie_count = 0
    path_list = []

    for m in movies_to_update:
        movie_count += 1
        path_list.append(m)

    main_window.write_event_value('-MOVCOUNT-', movie_count)
    movie_prog = 0

    print("about to go through files")

    for movies in path_list:
        # if main_window['-CANCEL-']:
        #     break
        start_update(movies, main_window, settings)
        movie_prog += 1
        main_window.write_event_value('-MOVEPROG-', movie_prog)


def batch_update(targets, main_window, settings):
    main_window.write_event_value('-MOVCOUNT-', len(targets))

    movie_prog = 0

    print(targets)

    for movies in targets:
        # if main_window['-CANCEL-']:
        #     break
        start_update(movies, main_window, settings)
        movie_prog += 1
        main_window.write_event_value('-MOVEPROG-', movie_prog)
