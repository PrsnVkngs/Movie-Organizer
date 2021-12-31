import subprocess

from get_tmdb_data import *
from get_movie_metadata import *


def start_update(path, movie):
    track_info = get_track_info(path, movie)
    movie_info = make_tmdb_call(movie)

    prop_cmd = 'mkvpropedit ' + "\"" + str(path + "\\" + movie) + "\"" + ' --edit info --set "title=' + movie_info[
        'title'] + "\""

    print(prop_cmd)

    # print(track_info)

    # print(track_info[3])

    for i in range(1, track_info[0] + 1):  # add the video track edits
        prop_cmd += ' --edit track:v' + str(i) + " --set codec-id=" + str(
            track_info[3][i - 1]['codec_id']) + ' --set codec-name=' + \
                    "\"" + str(track_info[3][i - 1]['commercial_name']) + "\"" + ' --set pixel-width=' + str(
            track_info[3][i - 1]['width']) + \
                    ' --set pixel-height=' + str(track_info[3][i - 1]['height']) + ' --set display-width=' + str(
            track_info[3][i - 1][
                'sampled_width']) + ' --set display-height=' + str(track_info[3][i - 1]['sampled_height'])

        # + ' --set bit-depth=' + str(track_info[3][i - 1]['bit_depth'])

    print(prop_cmd)

    for i in range(1, track_info[1] + 1):  # add the audio track edits
        prop_cmd += ' --edit track:a' + str(i) + " --set codec-id=" + str(
            track_info[4][i - 1]['codec_id']) + ' --set codec-name=' + \
                    "\"" + str(track_info[4][i - 1]['commercial_name']) + "\"" + ' --set language=' + \
                    str(track_info[4][i - 1]['language']) + \
                    ' --set channels=' + str(track_info[4][i - 1]['channel_s']) + ' --set sampling-frequency=' + str(
            track_info[4][i - 1]['sampling_rate'])

    print(prop_cmd)

    for i in range(1, track_info[2] + 1):  # add the audio track edits
        prop_cmd += ' --edit track:s' + str(i) + " --set codec-id=" + str(
            track_info[5][i - 1]['codec_id']) + ' --set codec-name=' + \
                    "\"" + str(track_info[5][i - 1]['commercial_name']) + "\"" + ' --set language=' + \
                    str(track_info[5][i - 1]['language'])

    print(prop_cmd)

    result = subprocess.run(prop_cmd, capture_output=True)
    print(result.stdout)


if __name__ == '__main__':
    start_update('O:\\Movies', 'Iron Man 2 (2010).mkv')
