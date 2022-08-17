import subprocess

"""
This is a wrapper class that will assist in using MKV prop edit. At the moment, it is very clunky.
It is quite hard to use and annoying to use in code. This wrapper will make it more modular so that one 
key error doesn't kill the update."""


def e_video_track(t_n):
    return f"--edit track:v{t_n} "


def e_audio_track(t_n):
    return f"--edit track:a{t_n} "


def e_sub_track(t_n):
    return f"--edit track:s{t_n} "


def e_codec_id(c_i):
    return f"--set codec-id=\"{c_i}\" "


def e_codec_name(c_n):
    return f"--set codec-name=\"{c_n}\" "


# video edits


def e_d_height(d_h):
    return f"--set display-height={d_h} "


def e_d_width(d_w):
    return f"--set display-width={d_w} "

# audio edits


def e_language(language):
    return f"--set language={language} "


def e_channels(ch_n):
    return f"--set channels={ch_n} "


def e_sampling_rate(s_r):
    return f"--set sampling-frequency={s_r} "


def e_bit_depth(b_d):
    return f"--set bit-depth={b_d} "
