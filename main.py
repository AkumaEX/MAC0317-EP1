import sys
import wave
import numpy as np
from synthesizer import Synthesizer

# preparando a estrutura de dados
adsr = open(sys.argv[1], 'r').readlines()
freq = int(sys.argv[2])
part = sys.stdin.readlines()

# amostragem da melodia
synt = Synthesizer(adsr, freq, part)
melody = synt.get_melody()

# estruturando a amostragem em 2 canais de 16 bits
audio = (melody*32768).astype(np.int16)
mono = np.reshape(audio, (len(audio), 1))
stereo = np.hstack((mono, mono))

# criando o arquivo .wav
with wave.open(sys.stdout.buffer, 'wb') as file:
    file.setnchannels(2)
    file.setsampwidth(2)
    file.setframerate(freq)
    file.writeframes(stereo)
