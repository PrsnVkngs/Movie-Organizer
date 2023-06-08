from pathlib import Path

from pymediainfo import MediaInfo as mI

# desired_info = {
#
#     "Video": ['codec_id', 'commercial_name', 'sampled_width', 'sampled_height'],
#     "Audio": ['codec_id', 'commercial_name', 'language', 'channel_s', 'sampling_rate', 'bit_depth'],
#     "Subtitles": ['codec_id', 'commercial_name', 'language'],
#
# }

unwanted_keys = ['other_', 'count', 'settings', '__', '_url', 'colour', '_version', 'transfer_', 'kind_of_stream',
                 'stream_identifier', 'streamorder', 'track_id', 'unique_id', 'format_info', 'format_profile',
                 'internet_media_type', 'duration', 'bit_rate']

mkvpropedit_keys = {'title', 'track_number', 'name', 'language', 'codec_id', 'codec_name', 'pixel_height',
                    'pixel_width', 'display_height', 'display_width', 'channels', 'bit_depth', 'track_type',
                    'chroma_siting_vertical', 'chroma_siting_horizontal'}

translations = {

    'format': 'codec_name',
    'commercial_name': 'codec_id',
    'channel_s': 'channels',
    'sampling_rate': 'sampling_frequency',
    'sampled_height': 'pixel_height',
    'sampled_width': 'pixel_width',
    'height': 'display_height',
    'width': 'display_width'

}


def filter_track(track_data):
    track_type = track_data['track_type']
    # negative filter
    # filtered_track = {key.replace('_', '-'): value for key, value in track_data.items() if not any(unwanted in key for unwanted in unwanted_keys)}
    match track_type:
        case 'Video':
            if 'chroma_subsampling' in track_data:
                chroma = track_data.pop('chroma_subsampling')
                chroma = chroma.split(':')
                track_data['chroma_siting_horizontal'] = chroma[1]
                track_data['chroma_siting_vertical'] = chroma[2]
                track_data.pop('bit_depth')

        case 'Audio':
            if 'title' in track_data:
                track_data.pop('title')

    for old_key in set(translations.keys()).intersection(track_data.keys()):
        key_value = track_data.pop(old_key)
        track_data[translations[old_key]] = key_value

    # positive filter
    # print(track_data.items())
    filtered_track = {key.replace('_', '-'): track_data[key] for key in mkvpropedit_keys if key in track_data.keys()}
    # print(filtered_track)
    return filtered_track


def get_track_info(path_to):
    """
    Given the directory location of a movie, this function will parse the file into MediaInfo and return the
    available video, audio and text track details. :param path: :param movie: :return: A list of data in dict form
    for the movie file. Elements 1-3 are counters to make it more easily known how many of each track there are.
    Video track is element 4, Audio track is element 5, Text track is element 6. There will be a string saying "not
    available" if media info does not find a track for that type.
    """
    mediainfo_dat = mI.parse(path_to.absolute())

    track_data = {'Video': [], 'Audio': [], 'Subtitles': []}

    for track in mediainfo_dat.tracks:
        track_type = track.track_type
        if track_type in track_data:
            track_data[track_type].append(filter_track(track.to_data()))

    for track_type in track_data:
        if not track_data[track_type]:
            track_data[track_type] = 0

    return track_data


if __name__ == '__main__':
    # elapsed_time = timeit.timeit(lambda: get_track_info(Path('E:/Life After Chernobyl (2016) [tmdbid=458970].mkv')), number=10)
    # info = get_track_info(Path('E:/Life After Chernobyl (2016) [tmdbid=458970].mkv'))
    movie = Path('O:/Movie/Tests/Secret Yellowstone (2007) [tmdbid=615333].mkv')
    track_info = get_track_info(movie)

    prop_cmd = f'mkvpropedit \"{movie.absolute()}\" --set \"title={"Secret Yellowstone"}\" '

    # for track in track_info.values():
    #     if track != 0:
    #         print(track)

    for track in track_info.values():
        if track != 0:
            for num, info in enumerate(track):
                t_type = info.pop('track-type')
                t_type = t_type[0].lower()
                prop_cmd += f"--edit track:{t_type}{num + 1} "
                for detail, value in info.items():
                    prop_cmd += f"--set {detail}=\"{value}\" "

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(prop_cmd)
    print(prop_cmd)

    # print(f"Elapsed time on SSD: {elapsed_time} seconds")

    # elapsed_time = timeit.timeit(lambda: get_track_info(Path('O:/Movie/Life After Chernobyl (2016) [tmdbid=458970].mkv')),number=10)
    # info = get_track_info(Path('O:/Movie/Life After Chernobyl (2016) [tmdbid=458970].mkv'))
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(info)

    # print(f"Elapsed time on HDD: {elapsed_time} seconds")
