import time

import numpy as np
import pyaudio
import scipy.io.wavfile as wavfile

from waveshaper import Waveshaper

# https://github.com/nrlakin/robot_voice

VB = 0.1
VL = 0.8

# Controls distortion
H = 2

# Controls N samples in lookup table; probably leave this alone
LOOKUP_SAMPLES = 1024

# Frequency (in Hz) of modulating frequency
MOD_F = 50


def diode_lookup(n_samples):
    result = np.zeros((n_samples,))

    for i in range(0, n_samples):
        v = abs((i - n_samples / 2) / (n_samples / 2))
        if v < VB:
            result[i] = 0
        elif VB < v <= VL:
            result[i] = H * ((v - VB) ** 2) / (2 * VL - 2 * VB)
        else:
            result[i] = H * v - H * VL + (H * (VL - VB) ** 2) / (2 * VL - 2 * VB)

    return result


def raw_diode(signal):
    result = np.zeros(signal.shape)

    for i in range(0, signal.shape[0]):
        v = signal[i]
        if v < VB:
            result[i] = 0
        elif VB < v <= VL:
            result[i] = H * ((v - VB) ** 2) / (2 * VL - 2 * VB)
        else:
            result[i] = H * v - H * VL + (H * (VL - VB) ** 2) / (2 * VL - 2 * VB)

    return result


def loop(data, *_, rate=16000, dtype=np.int16):
    # get max value to scale to original volume at the end
    data = np.fromstring(data, dtype=dtype)
    scaler = np.max(np.abs(data)) or 1

    if np.isnan(scaler):
        raise TypeError('Unexpected NaN in audio data.')

    # Normalize to floats in range -1.0 < data < 1.0
    data = data.astype(np.float) / scaler


    # Length of array (number of samples)
    n_samples = data.shape[0]

    # Create the lookup table for simulating the diode.
    d_lookup = diode_lookup(LOOKUP_SAMPLES)
    diode = Waveshaper(d_lookup)

    # Simulate sine wave of frequency MOD_F (in Hz)
    tone = np.arange(n_samples)
    tone = np.sin(2 * np.pi * tone * MOD_F / rate)

    # Gain tone by 1/2
    tone *= 0.5

    # Junctions here
    tone2 = tone.copy()  # to top path
    data2 = data.copy()  # to bottom path

    # Invert tone, sum paths
    tone = data2 - tone2  # bottom path
    data = data2 + tone2  # top path

    # top
    data = diode.transform(data) + diode.transform(-data)

    # bottom
    tone = diode.transform(tone) + diode.transform(-tone)

    result = data - tone

    # scale to +-1.0
    result /= np.max(np.abs(result)) or 1
    # now scale to max value of input file.
    result *= scaler

    return result, pyaudio.paContinue


if __name__ == '__main__':
    '''
    rate, data = wavfile.read('sample.wav')
    data = data[:,1]
    data = loop(data, rate=rate)
    wavfile.write('robot.wav', rate, data[0].astype(np.int16))
    '''
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=2,
        rate=16000,
        input=True,
        stream_callback=loop
    )

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)


