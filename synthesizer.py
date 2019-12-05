import re
import numpy as np


class Synthesizer:

    def __init__(self, adsr, freq, part):
        self._adsr = adsr
        self._freq = freq
        self._part = part

        def C(octave):
            return 16.352*2**int(octave)

        def Db(octave):
            return 17.324*2**int(octave)

        def D(octave):
            return 18.354*2**int(octave)

        def Eb(octave):
            return 19.445*2**int(octave)

        def E(octave):
            return 20.602*2**int(octave)

        def F(octave):
            return 21.827*2**int(octave)

        def Gb(octave):
            return 23.125*2**int(octave)

        def G(octave):
            return 24.500*2**int(octave)

        def Ab(octave):
            return 25.957*2**int(octave)

        def A(octave):
            return 27.500*2**int(octave)

        def Bb(octave):
            return 29.135*2**int(octave)

        def B(octave):
            return 30.868*2**int(octave)

        self._pitch = {
            'C': C,
            'C#': Db,
            'Db': Db,
            'D': D,
            'D#': Eb,
            'Eb': Eb,
            'E': E,
            'F': F,
            'F#': Gb,
            'Gb': Gb,
            'G': G,
            'G#': Ab,
            'Ab': Ab,
            'A': A,
            'A#': Bb,
            'Bb': Bb,
            'B': B,
        }

    def _get_freq(self, note):
        """Recebe uma notação alfabética e devolve a sua frequência"""
        [tone, octave, []] = re.split('(-?\d+)', note)
        return self._pitch[tone](octave)

    def _get_amp(self, T):
        """Recebe a duração do timbre e devolve sua amplitude"""
        num_samples = int(self._freq*T)
        a = np.linspace(start=0, stop=0, endpoint=True, num=num_samples)

        ta, la = np.float_(self._adsr[0].split())
        td, ld = np.float_(self._adsr[1].split())
        ts, ls = np.float_(self._adsr[2].split())
        tr, lr = np.float_(self._adsr[3].split())

        t0 = 0
        # attack
        t1 = int(num_samples*ta)
        t = np.linspace(start=0, stop=ta*T, endpoint=True,
                        num=int(num_samples*ta))
        a[t0:t1] = t * (la/(ta*T))

        # decay
        t2 = int(num_samples*td) + t1
        t = np.linspace(start=0, stop=td*T, endpoint=True,
                        num=int(num_samples*td))
        a[t1:t2] = t * (ld-la)/(td*T) + la

        # sustain
        t3 = int(num_samples*ts) + t2
        t = np.linspace(start=0, stop=ts*T, endpoint=True,
                        num=int(num_samples*ts))
        a[t2:t3] = t * (ls-ld)/(ts*T) + ld

        # release
        t4 = int(num_samples*tr) + t3
        t = np.linspace(start=0, stop=tr*T, endpoint=True,
                        num=int(num_samples*tr))
        a[t3:t4] = t * (lr-ls)/(tr*T) + ls

        return a

    def _get_sample(self, note, T):
        """Recebe uma notação alfabética e sua duração e devolve sua amostragem"""
        num_samples = int(self._freq*T)
        t = np.linspace(start=0, stop=T, endpoint=True, num=num_samples)
        k = self._get_freq(note)
        a = self._get_amp(T)
        return a * np.sin(2*np.pi*k*t)

    def get_melody(self):
        """Devolve a amostragem da melodia"""
        melody = []
        for i in range(1, len(self._part)):
            seq = self._part[i].split()
            T = int(re.split('(\n)', seq[len(seq)-1])[0])/1000
            for j in range(0, len(seq)-1):
                note = seq[j]
                sample = self._get_sample(note, T)
                melody = np.concatenate((melody, sample))
        return melody
