from pymediainfo import MediaInfo as mi


def get_track_info(path, movie):
    """
    Given the directory location of a movie, this function will parse the file into MediaInfo and return the
    available video, audio and text track details. :param path: :param movie: :return: A list of data in dict form
    for the movie file. Elements 1-3 are counters to make it more easily known how many of each tracks there are.
    Video track is element 4, Audio track is element 5, Text track is element 6. There will be a string saying "not
    available" if media info does not find a track for that type.
    """
    mediainfo_dat = mi.parse(path + "\\" + movie)

    video_track = []
    audio_track = []
    text_track = []

    video_track_count = 0
    audio_track_count = 0
    text_track_count = 0

    for track in mediainfo_dat.tracks:
        if track.track_type == "Video":
            video_track_count += 1
            video_track.append(track.to_data())

        elif track.track_type == "Audio":
            audio_track_count += 1
            audio_track.append(track.to_data())

        elif track.track_type == "Text":
            text_track_count += 1
            text_track.append(track.to_data())

    movie_metadata = [video_track_count, audio_track_count, text_track_count]

    if video_track_count == 0:
        movie_metadata.append("not available")
    else:
        movie_metadata.append(video_track)

    if audio_track_count == 0:
        movie_metadata.append("not available")
    else:
        movie_metadata.append(audio_track)

    if text_track_count == 0:
        movie_metadata.append("not available")
    else:
        movie_metadata.append(text_track)

    print(text_track)

    return movie_metadata


if __name__ == '__main__':
    get_track_info('O:\\Movies', 'Iron Man 2 (2010).mkv')
