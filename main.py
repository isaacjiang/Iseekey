from kivy.app import App
from kivy.core.window import Window

from datetime import datetime,time,timedelta
import time

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

import pyaudio
import wave

import speech_recognition as sr


class ClockLayout(FloatLayout):
    time_prop = ObjectProperty(None)
    input_text_prop = ObjectProperty(None)
    notice_text_prop = ObjectProperty(None)
    start_prop = ObjectProperty(None)


class ClockApp(App):
    sw_started = 0
    sw_seconds = 0

    def update_time(self,nap):
        now = datetime.now()
        self.root.time_prop.text = now.strftime('%H:%M:%S')
        self.root.stopwatch_prop.text = '00:00:00'

    def speech_input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:                # use the default microphone as the audio source
            audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
        try:
            t = r.recognize(audio)
        except LookupError:
            t = ' '
        return t

    def start_stop(self):
        if self.sw_started == 2:
           self.sw_seconds = 0
        if self.sw_started in (0,2):
            input_text = self.speech_input()
            self.root.input_text_prop.text = input_text
            try:
                self.sw_seconds = int(input_text)
                self.root.start_prop.text = ('Got it')
                self.root.notice_text_prop.text = ('The Stopwatch will stop after '+input_text + ' Seconds')
                self.sw_started = 1
            except ValueError:
                self.root.notice_text_prop.text = ('Please say a number')
                self.root.start_prop.text = ('Try again')
            return
        else:
            self.root.start_prop.text = ('Again')
            Clock.schedule_interval(self.start_stopwatch, 0.016)
            self.sw_started = 2


    def start_stopwatch(self, nap):
        if int(self.sw_seconds) >= 1:
            self.sw_seconds -= nap
            minutes, seconds = divmod(self.sw_seconds, 60)
            self.root.stopwatch_prop.text = (
                '%02d:%02d:%02d' %(int(minutes), int(seconds)-2,int(seconds * 100 % 100)))
            if int(self.sw_seconds) == 1 :
                self.play_audio()
                self.root.start_prop.text = ('Start')
                self.root.notice_text_prop.text = ('Please Start. ')
                self.sw_seconds = 0
        else:
            return

    def play_audio(self):
         #define stream chunk
         chunk = 1024
         #open a wav format music
         f = wave.open(r'audio/doublebass.wav','rb')
         p = pyaudio.PyAudio()
         stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                channels = f.getnchannels(),
                rate = f.getframerate(),
                output = True)
         data = f.readframes(chunk)
         while data != '':
             stream.write(data)
             data = f.readframes(chunk)
         p.terminate()

    def on_start(self):
        self.root.notice_text_prop.text = ('Please Start.')
        Clock.schedule_interval(self.update_time, 1)



if __name__ == '__main__':
    from kivy.utils import get_color_from_hex
    Window.clearcolor = get_color_from_hex('#888888')
    ClockApp().run()

