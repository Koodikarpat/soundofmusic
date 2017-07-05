from typing import Union
import collections
import audioop
import sys
import os

from pocketsphinx import Decoder
from fuzzywuzzy import process
import pyaudio


class VoiceDetector:

    """
    A class for detecting speech
    """
    def __init__(self, *, chunk: int = 1024, rate: int = 16000,
                 channels: int = 1,
                 data_format=pyaudio.paInt16,
                 model_dir: str = 'pocketsphinx/model',
                 data_dir: str = 'pocketsphinx/test/data',
                 stream=None):
        self.data_format = data_format
        self.model_dir = model_dir
        self.data_dir = data_dir
        self.channels = channels
        self.chunk = chunk
        self.rate = rate

        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(self.model_dir, 'en-us/en-us'))
        config.set_string('-lm', os.path.join(self.model_dir, 'en-us/en-us.lm.bin'))
        config.set_string('-dict', os.path.join(self.model_dir, 'en-us/cmudict-en-us.dict'))
        location = 'NUL' if sys.platform.startswith('win') else '/dev/null'
        config.set_string('-logfn', location)
        self.decoder = Decoder(config)

        # Configure a pyaudio stream or use the provided one
        if stream is None:
            p = pyaudio.PyAudio()
            self.stream = p.open(frames_per_buffer=self.chunk,
                                 channels=self.channels,
                                 format=self.data_format,
                                 rate=self.rate,
                                 input=True)
        else:
            self.stream = stream

        self.threshold = self.get_threshold()

        self.silence_buffer = collections.deque(maxlen=self.rate // self.chunk)
        self.buffer = []

    def get_threshold(self, samples=50) -> int:
        # threshold is the average of 1/5 of the loudest samples
        values = sorted([abs(audioop.avg(self.stream.read(self.chunk), 4)) ** 0.5 for _ in range(samples)], reverse=True)
        valid = slice(None, int(samples * 0.2))
        threshold = max(1000, int(sum(values[valid]) / (samples * 0.2)) + 100)

        print('Threshold set at: {}'.format(threshold))
        return threshold

    def decode(self, buffer: list) -> Union[str, None]:
        if not buffer:
            return

        # try recognizing speech from buffer
        self.decoder.start_utt()
        for entry in buffer:
            self.decoder.process_raw(entry, False, False)
        self.decoder.end_utt()

        # either the words recognized or None if no words were recognized
        hyp = self.decoder.hyp()

        if hyp is None:
            return
        else:
            return hyp.hypstr

    def poll(self, data=None):
        data = data or self.stream.read(self.chunk)
        self.silence_buffer.append(abs(audioop.avg(data, 4)) ** 0.5)

        talking = any(val > self.threshold for val in self.silence_buffer)

        if talking:
            self.buffer.append(data)
        else:
            command = self.decode(self.buffer)
            self.buffer.clear()

            if command:
                print(command)
                self.invoke(command)

    def run(self):
        while True:
            self.poll()

    def invoke(self, command: str):
        commands = {
            'play': self.play
        }
        command, *args = command.split()
        closest_command, certainty = process.extractOne(command, commands.keys())

        if certainty < 90:
            return

        commands[closest_command](args)

    def play(self, args: list):
        if not os.path.exists('songs'):
            print("lahslkjg sjkdgh lkasdglku")
            return

        songs = os.path.listdir('songs')
        name = ' '.join(args)

        best_match = process.extractOne(name, songs)

        print(best_match)


if __name__ == '__main__':
    v = VoiceDetector()
    v.run()
