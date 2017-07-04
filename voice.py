from typing import Union
from os import path
import collections
import audioop
import sys

from pocketsphinx import Decoder
import pyaudio


class VoiceDetector:
    """
    A class for detecting speech
    """
    def __init__(self, *, chunk: int = 1024, rate: int = 16000,
                 channels: int = 1,
                 data_format=pyaudio.paInt16,
                 model_dir='pocketsphinx/model',
                 data_dir='pocketsphinx/test/data'):
        self.data_format = data_format
        self.model_dir = model_dir
        self.data_dir = data_dir
        self.channels = channels
        self.chunk = chunk
        self.rate = rate

        config = Decoder.default_config()
        config.set_string('-hmm', path.join(self.model_dir, 'en-us/en-us'))
        config.set_string('-lm', path.join(self.model_dir, 'en-us/en-us.lm.bin'))
        config.set_string('-dict', path.join(self.model_dir, 'en-us/cmudict-en-us.dict'))
        location = 'NUL' if sys.platform.startswith('win') else '/dev/null'
        config.set_string('-logfn', location)
        self.decoder = Decoder(config)

        p = pyaudio.PyAudio()
        self.stream = p.open(frames_per_buffer=self.chunk,
                             channels=self.channels,
                             format=self.data_format,
                             rate=self.rate,
                             input=True)

        self.threshold = self.get_threshold()

    def get_threshold(self, samples=50) -> int:
        values = sorted([abs(audioop.avg(self.stream.read(self.chunk), 4)) ** 0.5 for _ in range(samples)], reverse=True)
        print(values)
        valid = slice(None, int(samples * 0.2))
        print(int(sum(values[valid])))
        threshold = max(700, int(sum(values[valid]) / (samples * 0.2)) + 100)

        print('Threshold set at: {}'.format(threshold))
        return threshold

    def decode(self, data: list) -> Union[str, None]:
        if not data:
            return

        self.decoder.start_utt()
        for entry in data:
            self.decoder.process_raw(entry, False, False)
        self.decoder.end_utt()

        hyp = self.decoder.hyp()

        if hyp is None:
            return
        else:
            return hyp.hypstr

    def run(self):
        silence_buffer = collections.deque(maxlen=self.rate // self.chunk)
        buffer = []

        while True:
            data = self.stream.read(self.chunk)
            silence_buffer.append(abs(audioop.avg(data, 4)) ** 0.5)

            talking = any(val > self.threshold for val in silence_buffer)

            if talking:
                buffer.append(data)
            else:
                print(self.decode(buffer))
                buffer.clear()


if __name__ == '__main__':
    v = VoiceDetector()
    v.run()
