

import speech_recognition as sr
import pyaudio
import wave
import threading
from kivy.storage.jsonstore import JsonStore


class SpeechInput(threading.Thread):

    def __init__(self, group=None, target=None, name=None,args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            t = r.recognize(audio)
        except LookupError:
            t = ' '
        self.args.ids['input_speech'].text = t
        self.args.ids['gsra_start'].text = 'Again'
        print t


class PlayAudio(threading.Thread):
    CHUNK = 1024

    def __init__(self,group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs

        filename = self.kwargs['filename']
        self.filename = filename
        self.wf = wave.open(self.filename, 'rb')
        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(format = self.player.get_format_from_width(self.wf.getsampwidth()),
            channels = self.wf.getnchannels(),
            rate = self.wf.getframerate(),
            output = True,
            stream_callback=self.callback_set_color)

        super(PlayAudio, self).__init__()
        self._stop = threading.Event()

    def callback_set_color(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)

        descript = JsonStore('data_descript.json')
        cwd = str(descript.get(self.kwargs['filename'])['desc'])
        self.kwargs['root'].ids['cw_desc'].text = '[color=000000] ' + cwd + '[/color]'
        cwd_list = str.split(cwd)
        progress = int(round(float(self.wf.tell())/float(self.wf.getnframes()),2)*cwd_list.__len__())
        cwd_list.insert(0, '[color=ff3333]')
        cwd_list.insert(progress+1, '[/color]')
        cwd_markup = ''
        for i in range(cwd_list.__len__()):
            cwd_markup = cwd_markup + cwd_list[i] + ' '
        self.kwargs['root'].ids['cw_desc'].text = cwd_markup
        #print progress
        if self.Playstate is True:
            return (data,pyaudio.paContinue)
        else:
            return (data,pyaudio.paComplete)

    def run(self):
        self.Playstate = True

    def stop(self):
        self.Playstate = False
        # stop stream (6)
        self.stream.stop_stream()
        self.stream.close()
        self.wf.close()
        # close PyAudio (7)
        self.player.terminate()

    def playback(self, backtime):
        self.stream.stop_stream()
        self.wf.setpos(self.wf.tell()-backtime)
        self.stream.start_stream()


class Grading():

    def get_grade(self,filename, root):

        descript = JsonStore('data_descript.json')
        cwd = str(descript.get(filename)['desc'])
        speech = root.ids['input_speech'].text
        cwd_list = str.split(cwd)
        speech_list = str.split(speech)
        correct = set(cwd_list).intersection(speech_list)
        correct_number = len(correct)

        if correct_number <= 10:
            marks = correct_number * correct_number
        else:
            marks = correct_number * 10
        return marks

import md5
import sys

class PasswordCheck():
    # i already made an md5 hash of the password: PASSWORD
    password = "319f4d26e3c536b5dd871bb2c52e3178"

    def check_password(self):
        for key in range(3):
            #get the key
            p = raw_input("Enter the password >>")
            #make an md5 object
            mdpass = md5.new(p)
            #hexdigest returns a string of the encrypted password
            if mdpass.hexdigest() == self.password:
                #password correct
                return True
            else:
                print 'wrong password, try again'
        print 'you have failed'
        return False