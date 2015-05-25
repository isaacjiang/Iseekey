

import speech_recognition as sr
import pyaudio as pa
import wave as wv
from kivy.core.video import Video
import pygame
from pygame import movie


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

    def play_audio(self):
         chunk = 1024                                  #define stream chunk
         f = wv.open(r'audio/doublebass.wav','rb')     #open a wav format music
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





