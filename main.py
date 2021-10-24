import os
import shutil

import librosa

import engine


if __name__ == "__main__":
    shutil.rmtree("cache", ignore_errors=True)
    os.mkdir("cache")
    y, sr = librosa.load("a.wav")
    engine.freq(engine.filename)
    #engine.resample_audio(engine.filename, 1, 57)
