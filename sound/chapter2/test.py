from manim import *
import math
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
from pathlib import Path
from scipy.io import wavfile

SR = 48000


class WaveType(Enum):
    SINE = 0
    SQUARE = 1
    TRIANGLE = 2
    SAW = 3


class AudioGenerator:
    def __init__(self, f=440.0, v=0, type=WaveType.SINE):
        self.f_i = f
        self.f_f = f
        self.v_i = v
        self.v_f = v
        self.type = type
        self.last_val = 0.0
        self.second_last_val = 0.0

    def __repr__(self):
        return f"\
        Freq: {self.f_i} {self.f_f}\
        Volume: {self.v_i} {self.v_f}\
        "

    def volume_filter(self, dur, v):
        num_samples = int(SR * dur)
        if self.v_f == 0:
            self.v_f = 0.00001
        if v == 0:
            v = 0.00001

        buffer = np.geomspace(self.v_f, v, endpoint=True, num=num_samples)
        return buffer

    def decibelToGain(self, db):
        if db > -math.inf:
            return pow(10.0, db * 0.05)
        else:
            return 0

    def freq_interp(self, dur, freq, use_last_val=True):
        num_samples = int(SR * dur)
        log_f1 = np.log10(self.f_i)
        log_f2 = np.log10(freq)
        f = np.linspace(log_f1, log_f2, num_samples)
        phi = 0.0
        if use_last_val:
            phi = np.arccos(self.last_val)
            if self.second_last_val > self.last_val:
                phi *= -1.0

        samples = np.cos(2 * np.pi * np.cumsum(pow(10, f) / SR) - phi)
        self.last_val = samples[-1]
        self.second_last_val = samples[-2]
        return samples

    def next(self, duration=1.0, f=440, v=0.5, use_last_val=True):
        self.f_i = self.f_f
        self.f_f = f
        x = self.freq_interp(duration, f, use_last_val=use_last_val)
        x *= self.volume_filter(duration, v)
        self.v_i = self.v_f
        self.v_f = v
        return x


# shifts = [(5,20)]
# shifts = [(5, 20), (881, 440), (881, 440)]
# sound0 = AudioGenerator(5)
# sound1 = AudioGenerator(20)
# t = np.linspace(0, len(shifts), 48000 * len(shifts))
# final0 = np.concatenate([sound0.next(1, shift[0], 0) for shift in shifts])
# final1 = np.concatenate([sound0.next(1, shifts[i][1], i) for i in range(len(shifts))])

# final = final0 + final1

fig, ax1 = plt.subplots(nrows=1, ncols=1)
ax1.plot(t, final)
ax1.set_title("Curve")
plt.show()
