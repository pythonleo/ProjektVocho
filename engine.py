import os
import subprocess
import wave
import statistics
from math import ceil

import librosa
import soundfile
import numpy
import scipy.io.wavfile


filter_low = 430 # Not sure of its purpose, mentioned in utau_output.txt
voicebank = "lty"
filename = "a.wav"


def freq(fname):
    time_list = []
    freq_list = []
    aubio_path = ""
    if os.name == "nt":
        aubio_path = "tools/aubio/aubiopitch.exe"
    else:
        aubio_path = "aubiopitch"
    s = subprocess.run("%s \"%s\" -H 1024 -u midi" % (aubio_path, fname), \
                       capture_output=True)
    output = s.stdout.decode().split('\n')
    for i in range(1, len(output)):
        if output[i]:
            time_list.append(output[i].split()[0])
            freq_list.append(round(float(output[i].split()[1]), 2))
    return time_list, freq_list


def resample_audio(fname, time_rate, target_pitch):
    # Cut the audio into small pieces to essentially
    # "flatten" out the waveform
    ffmpeg_path = ""
    if os.name == "nt":
        ffmpeg_path = "powershell.exe tools/ffmpeg/ffmpeg.exe"
    else:
        ffmpeg_path = "ffmpeg"
    time_list, freq_list = freq(fname)
    time_list = time_list[1:]
    freq_list = freq_list[1:]
    time_strs = ",".join(time_list)
    cache_name = "cache/{0}_%d.wav".format(fname)
    cmd = "%s -i %s -f segment -segment_times %s -c copy \"%s\"" % \
          (ffmpeg_path, fname, time_strs, cache_name)
    s = subprocess.run(cmd, capture_output=True)

    # Process each segment of the audio, applying a universal
    # `time_rate` and a different `pitch_rate`.
    # `txt_fname` tells ffmpeg which files to concat after
    # individual tuning is over
    txt_fname = "cache/%s_%s_%d.txt" % (voicebank, fname, target_pitch)
    target_fname = "cache/%s_%s_%d.wav" % (voicebank, fname, target_pitch)
    f = open(txt_fname, "w")
    y, sr = librosa.load(fname, sr=44100, mono=True)
    for i in range(len(freq_list)):
        cache_name = "cache/%s_%d.wav" % (fname, i)
        try: y, sr = librosa.load(cache_name, sr=44100, mono=True)
        except: break
        pitch_rate = target_pitch - freq_list[1]
        target = librosa.effects.pitch_shift(y, sr, pitch_rate / 2)
        cache_name = "%s_%s_%d_%d.wav" % \
                    (voicebank, fname, target_pitch, i)
        soundfile.write("cache/%s" % cache_name, target, sr)
        f.write("file '%s'\n" % cache_name)
    cmd = "%s -f concat -safe 0 -i %s -c copy %s" % \
          (ffmpeg_path, txt_fname, target_fname)
    print(cmd)
    s = subprocess.call(cmd)
    y, sr = librosa.load(target_fname)
    librosa.effects.time_stretch(y, rate)