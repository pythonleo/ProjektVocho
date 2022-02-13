"""The heart of Projekt Vocho. Registers voice banks and manipulates them.

The engine supports both a "native" synthesizer and compatibility for
"resampler.exe"s used by UTAU on Windows.
"""

import os.path

import PySimpleGUI as psg


FILTER_LOW = 430
CURRENT_MODE = 0  # 0 - PV; 1 - resampler.exe (Windows only)
psg.theme("Default1")


def _register(path: str):
    """Register a voice library. Alert the user on failure. Auxiliary function.

    :param path: path to the voice bank (e.g. /path/to/voice/geping)
    :return: normcase()'d canonical path on success, empty string on failure
    """
    if not os.path.isdir(path):
        psg.popup("Voice bank not found or invalid",
                  "The voice bank \"" + path + "\" is not a valid voice bank "
                  "and therefore is not registered.\n"
                  "This warning can be disabled in Tools > Settings > "
                  "Voice Banks")
        return ""
    path = os.path.normcase(os.path.realpath(path))
    return path + "\n"


def register(path: str):
    """Add voice bank directory to voiebanks.txt

    :param path: path to the voice bank
    :return: void
    """
    f = open("../voicebanks.txt", "a+")
    f.write(path + "\n")
    f.close()


def cleanup():
    """Clean up voicebanks.txt by removing invalid/repetitive directories.

    :return: void
    """
    f = open("../voicebanks.txt", "r+")
    voicebank_list = []
    for item in f.readlines():
        item = item.rstrip()
        voicebank_list.append(_register(os.path.realpath(item)))
    f.seek(0)
    f.write("".join(set(sorted(voicebank_list))))
    f.truncate()
    f.close()


def resample(filename, target_time: float, target_pitch: int, **kwargs):
    """Wrapper for psola and resampler.exe to make things clean

    :param filename: filename of the base audio file
    :param target_time: target time in seconds (w/o BPM calculations)
    :param target_pitch: target pitch in MIDI number
    :param kwargs: additional parameters, in a both UTAU- and VOCALOID-
                   compatible format; passed to resampler.exe in mode 1
    :return: void, but outputs audio file in a cache folder
    """
    pass
