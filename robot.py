import pyo

from ringmod import RingMod

server = pyo.Server(duplex=1, nchnls=1)
server.boot()

mic = pyo.Input(0)
mic.ctrl(title='Device')
mic.out()

a = pyo.FreqShift(mic, shift=50)
a.ctrl(title='Pitch shift')
a.out()

r = RingMod(a, freq=45)
r.out()
r.ctrl(title='Ring modulator 1')

r2 = RingMod(r, freq=100)
r2.out()
r2.ctrl(title='Ring modulator 2')

server.start()
server.gui(locals())
