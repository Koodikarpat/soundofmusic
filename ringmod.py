"""
Taken from http://ajaxsoundstudio.com/pyodoc/tutorials/pyoobject1.html?highlight=ring
"""
from pyo import *


class RingMod(PyoObject):
    def __init__(self, input, freq=100, mul=1, add=0):
        super().__init__(mul, add)
        self._input = input
        self._freq = freq
        self._in_fader = InputFader(input)
        in_fader, freq, mul, add, lmax = convertArgsToLists(
            self._in_fader, freq, mul, add
        )
        self._mod = Sine(freq=freq, mul=in_fader)
        self._ring = Sig(self._mod, mul=mul, add=add)
        self._base_objs = self._ring.getBaseObjects()

    def setInput(self, x, fadetime=0.05):
        self._input = x
        self._input_fader.setInput(x, fadetime)

    def setFreq(self, x):
        self._freq = x
        self._mod.freq = x

    def play(self, dur=0, delay=0):
        self._mod.play(dur, delay)
        return super().play(dur, delay)

    def stop(self):
        self._mod.stop()
        return super().stop()

    def out(self, chnl=0, inc=1, dur=0, delay=0):
        self._mod.play(dur, delay)
        return super().out(chnl, inc, dur, delay)

    def ctrl(self, map_list=None, title=None, wxnoserver=False):
        self._map_list = [SLMap(10, 2000, 'log', 'freq', self._freq),
                          SLMapMul(self._mul)]
        super().ctrl(map_list, title, wxnoserver)

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, x):
        self.setInput(x)

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, x):
        self.setFreq(x)

