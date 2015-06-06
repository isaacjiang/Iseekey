__author__ = 'isaacjiang'

from kivy.app import App
import kivy.properties as prop
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListView
from kivy.adapters.dictadapter import DictAdapter
from kivy.storage.dictstore import DictStore
import model,functions
import pyaudio as pa
import wave as wv
import speech_recognition as sr

class cwListView(ListView):

    def __init__(self, **kwargs):
        cwdata = model.data()
        cw = cwdata.Coursework()
        args_converter = \
            lambda row_index, rec: {'text': rec['text'],
                                    'is_selected': rec['is_selected'],
                                    'size_hint_y': 0.5,
                                    'height': 60}

        cw_adapter = DictAdapter(data=cw,
                                 args_converter=args_converter,
                                 sorted_keys=cw.keys(),
                                 template='cwListItem')
        super(cwListView, self).__init__(adapter=cw_adapter)
        cw_adapter.bind(on_selection_change=self.callback)

    def callback(self, adapter):
        if len(adapter.selection) == 0:
            print "No selected item"
        else:
            selected_data = model.data()
            selected_cw_desc = selected_data.CwPlaying_desc()
            selected_cw_file = selected_data.CwPlaying_file()
            cw_name = adapter.selection[0].text
            cw_desc = selected_cw_desc[adapter.selection[0].text]
            cw_file = selected_cw_file[adapter.selection[0].text]
            ds = DictStore('temp')
            ds.put('select_cw_desc', name=cw_name, desc=cw_desc)
            ds.put('select_cw_file', name=cw_name, file=cw_file)


class AdScreen(Screen):
    pass

class SignScreen(Screen):
    pass

class CategoryScreen(Screen):
    pass

class WorkingScreen(Screen):
    pass

class IseekeyApp(App):
    icon = 'image/logo1.png'

    def build(self):
        root = ScreenManager()
        root.add_widget(AdScreen(name='Ad'))
        root.add_widget(SignScreen(name='sign'))
        root.add_widget(CategoryScreen(name='category'))
        root.add_widget(WorkingScreen(name='working'))
        return root

    def on_start(self):
        pass

    def sign_in(self):
        from django.contrib.auth import authenticate
        user = authenticate(username='isaacjiang', password='isaacjiang')
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")

    def get_cw(self, screen):
        ds = DictStore('temp')
        cwd = ds.get('select_cw_desc')['desc']
        screen.current_screen.ids['cw_desc'].text = cwd

    def gsra_start(self,screen):

        r = sr.Recognizer()
        with sr.Microphone() as source:                # use the default microphone as the audio source
            audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
        try:
            screen.current_screen.ids['input_speech'].text = r.recognize(audio)
        except LookupError:
            screen.current_screen.ids['input_speech'].text = ' '

    def play_origin(self, screen):
        ds = DictStore('temp')
        cwf = ds.get('select_cw_file')['file']
        chunk = 1024                                  #define stream chunk
        f = wv.open(r'audio/'+cwf, 'rb')     #open a wav format music
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

if __name__ == '__main__':
    IseekeyApp().run()
