

import speech_recognition as sr
import pyaudio as pa
import wave as wv
from kivy.storage.dictstore import DictStore
import threading
import time

class SpeechInput():
    def speech_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:                # use the default microphone as the audio source
            audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
        try:
            t = r.recognize(audio)
        except LookupError:
            t = ' '
        return t

class Play():
    def play_audio(self,filename):
         chunk = 1024                                  #define stream chunk
         f = wv.open(r''+filename,'rb')     #open a wav format music
         p = pa.PyAudio()
         stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                channels = f.getnchannels(),
                rate = f.getframerate(),
                output = True)
         data = f.readframes(chunk)
         while data != '':
             stream.write(data)
             data = f.readframes(chunk)
         p.terminate()

class audio():

    def __init__(self):
        pass

    def load(self, state):
        ds = DictStore('temp')
        cwf = ds.get('select_cw_file')['file']

        from kivy.core.audio import SoundLoader
        sound = SoundLoader.load('audio/'+cwf)
        if sound:
            if state == 'play':
                sound.play()
                print sound.source
            elif state == 'stop':
                sound.load()
                sound.stop()
                print sound.get_pos()
            else:
                print sound.get_pos()

    def play(self):
        thr1 = threading.Thread(target=self.load)
        thr1.start()

    def play_back(self):
        thr2 = threading.Thread(target=self.load)
        thr2.start()




