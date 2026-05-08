import numpy as np
from scipy.io.wavfile import write
import os

def generate_music(emotion, output_path="temp_music.wav", duration=10, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))

    if emotion == "joy":
        freq = 440  # A4 (bright)
    elif emotion == "fear":
        freq = 220  # low tone (dark)
    elif emotion == "action":
        freq = 330  # energetic
    elif emotion == "sad":
        freq = 180
    else:
        freq = 260

    audio = 0.2 * np.sin(2 * np.pi * freq * t)

    audio = (audio * 32767).astype(np.int16)

    write(output_path, sample_rate, audio)

    return output_path
















