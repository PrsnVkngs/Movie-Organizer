from pymediainfo import MediaInfo as mi


def get_track_info(movie):
    mediainfo_dat = mi.parse(movie)

    video_track = []
    audio_track = []

    video_track_count = 0
    audio_track_count = 0
    for track in mediainfo_dat.tracks:
        if track.track_type == "Video":
            video_track_count += 1
            video_track.append(
                {
                    "track_no": video_track_count,
                    "height": track.height,
                    "width": track.width,
                    "format": track.format,
                    "duration": track.other_duration[0],
                    "bit_rate": track.bit_rate,
                    "simple_bit_rate": track.other_bit_rate,
                    "frame_rate": track.frame_rate,
                    "bit_depth": track.bit_depth,
                    "simple_bit_depth": track.other_bit_depth
                }
            )
        elif track.track_type == "Audio":
            audio_track_count += 1
            audio_track.append(
                {
                    "track_no": audio_track_count,
                    "format": track.format,
                    "alt_format": track.other_format,
                    "easy_format": track.commercial_name,
                    "duration": track.other_duration[0],
                    "bit_rate": track.bit_rate,
                    "easy_bit_rate": track.other_bit_rate[0],
                    "bit_rate_mode": track.bit_rate_mode,
                    "channels": track.channel_s,
                    "sampling_rate": track.sampling_rate,
                    "easy_sampling_rate": track.other_sampling_rate[0],
                    "compression_mode": track.compression_mode,
                    "title": track.title,
                    "language": track.language,
                    "easy_language": track.other_language[0]
                }
            )

        elif track.track_type == "Text":
            print(track.language)
            print(track.other_language)
