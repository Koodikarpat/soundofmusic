#haluamme muokata ääntä, jonka koodi saa.
# 1. ääni tulee mikrofoonista, tallennetaan ääni ja tehdään sille muokkaus ja laitetaan ulos äänenä.
#-> viive

import librosa
import pyaudio
import wave
import IPython.display
import ffmpeg_normalize
import ffmpy
import os, os.path
# ffmpeg pitää saada toimimaan


aan = "C:\\Users\OGL\PycharmProjects\äänijuttu\\test_music.wav"
tln = "C:\\Users\OGL\PycharmProjects\äänijuttu\\temp_aani.wav"
tln2 = "C:\\Users\OGL\PycharmProjects\äänijuttu\\temp_aani2.wav"

ffmpy.FFmpeg("-hide_banner")


class AanenMuokkausclass:

    y, sr = librosa.load(aan,duration=10)

    def aanenmuokkaus(self):
        self.y_pitch = librosa.effects.pitch_shift(self.y,self.sr, n_steps=-8.0)


    def aanentallennus(self):
        # Huom. tallentaa äänen jotenkin typerästi -> pakko konvertoida FFMpegillä
        librosa.output.write_wav(tln, self.y_pitch, self.sr)

    def konvertoi_wav(self):
        # tämä konvertoi wav tiedoston toimivaan muotoon
        ff = ffmpy.FFmpeg(inputs={tln: None}, outputs={tln2: None})
        #ffmpeg ei ala konvertoimaan, jos sen pitää ylikirjoittaa (kai sillekkin löytyisi joku komento että se hyväksyy
        #sen, mutta tehdään nyt näin tässä vaiheessa.
        #if tln2:
        #    os.remove(tln2)
        #else:
        if os.path.isfile(tln2):
            os.remove(tln2)
            ff.run()
        else:
            ff.run()



# pyöritetään pääohjelma, eli äänen avaus, muokkaus ja tallennus uuteen tiedostoon


def main():

    aa = AanenMuokkausclass()
    aa.aanenmuokkaus()
    aa.aanentallennus()
    aa.konvertoi_wav()

# määritetään äänen toisto funktio. -> pitää saada toimimaan että voi testata äänenmuunninta.
# -> Ei toimi koska librosa ilmeisesti tallentaa äänen väärässä muodossa
# (windows kuitenkin toistaa sen ihan tavallisesti)
# --> jos ongelma on librosassa, tallennus funktiota pitää muuttaa. mutta jos vika onkin
# wavessa ja pyaudiossa eli niiden yhteensopivuudessa librosan kanssa, pitää keksiä joku toinen äänen toisto systeemi.
#


def toista2():
    y, sr = librosa.load(r"C:\\Users\OGL\PycharmProjects\äänijuttu\\test_music.mp3")
    IPython.display.Audio(data=y, rate=sr)

def toista():
    chunk = 1024
    f = wave.open(tln2, "rb")

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)

    data = f.readframes(chunk)

    while data:
        stream.write(data)
        data = f.readframes(chunk)

    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()


main()
toista()
