import os
import subprocess
import wave
import statistics
from math import ceil

import librosa
import soundfile
import numpy
import scipy.io.wavfile


filter_low = 430
voicebank = "geping"
filename = "a.wav"

""" W/o slicing, bad
def freq(fname):
    freq_list = []
    if os.name == "nt":
        s = subprocess.run("aubio-win/bin/aubiopitch.exe %s" % fname, capture_output=True)
        output = s.stdout.decode().split('\n')
        for line in output:
            if line:
                freq_list.append(round(float(line.split()[1]), 2))
        return statistics.median(freq_list)
    else:
        return 0


def resample_audio(fname: str, target_len, target_note):
    y, sr = librosa.load(fname, mono=True)
    src_len = librosa.get_duration(y, sr)
    rate = target_len / src_len
    avg_freq = freq(fname)
    print(avg_freq)
    avg_note = int(librosa.hz_to_midi(avg_freq))   # In MIDI for easy semitones
    print(avg_note, target_note)
    print(librosa.midi_to_note(avg_note), librosa.midi_to_note((target_note)))
    pitch_rate = target_note - avg_note
    target = librosa.effects.time_stretch(y, rate)
    target = librosa.effects.pitch_shift(y, sr, pitch_rate / 2)
    return target, sr
"""

""" Done w/ rubberband, not much better
def resample_audio(fname: str, target_len, target_note):
    target_hz = librosa.midi_to_hz(target_note)
    freq_rate = target_hz / freq("voice/%s/%s" % (voicebank, fname))
    cache_fname = "cache/%s-%s-%d-%d.wav" % \
                  (voicebank, fname, target_note, target_len)
    if os.name == "nt":
        subprocess.run("rubberband-win/rubberband.exe -c 5 -F -D %f -f %f %s %s" % \
                       (target_len, freq_rate, "voice/%s/%s" % \
                        (voicebank, fname), cache_fname))
    else:
        return
"""


def trim(start, end):
    # TODO: write some ffmpeg garbage
    pass


def freq(fname):
    time_list = []
    freq_list = []
    aubio_path = ""
    if os.name == "nt":
        aubio_path = "aubio-win/bin/aubiopitch.exe"
    else:
        aubio_path = "aubiopitch"
    s = subprocess.run("%s %s" % (aubio_path, fname), capture_output=True)
    output = s.stdout.decode().split('\n')
    for i in range(1, len(output)):
        if output[i]:
            time_list.append([output[i - 1].split()[0], output[i].split()[0]])
            freq_list.append(round(float(output[i].split()[1]), 2))
    return time_list, freq_list