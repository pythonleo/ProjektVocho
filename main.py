import os
import shutil

import librosa

import engine


if __name__ == "__main__":
    engine.resample_audio(engine.filename, 1, librosa.note_to_midi("A4"))
