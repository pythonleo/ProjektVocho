import librosa.display
import numpy as np

y, sr = librosa.load("misc/A4-440.0.wav", duration=15)
f = librosa.fft_frequencies(sr, n_fft=32768)
f0 = librosa.yin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
print(librosa.stft(y, n_fft=32768))
