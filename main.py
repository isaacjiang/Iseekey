__author__ = 'isaacjiang'

from kivy.app import App
import kivy.properties as prop
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.listview import ListView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.adapters.dictadapter import DictAdapter
from kivy.storage.dictstore import DictStore
import model,functions
from kivy.clock import Clock
import speech_recognition as sr
from functools import partial
import os

class flListView(ListView):

    datadir = os.getcwd()+'/data'
    level = 1

    def __init__(self, **kwargs):
        self.level = self.level+ 1
        subdirs={}
        if self.level <= 2:
            for subfolder in os.listdir(self.datadir):
                if os.path.isdir(os.path.join(self.datadir,subfolder)):
                    subdirs[os.path.join(self.datadir,subfolder)] = {'text': subfolder,'is_selected': False}
        else:
            for subfolder in os.listdir(self.datadir):
                subdirs[os.path.join(self.datadir,subfolder)] = {'text': subfolder,'is_selected': False}
        args_converter = \
            lambda row_index, rec: {'text': rec['text'],
                                    'is_selected': rec['is_selected'],
                                    'size_hint_y': 10,
                                    'height': 40}
        fl_adapter = DictAdapter(data=subdirs,
                                 args_converter=args_converter,
                                 sorted_keys=subdirs.keys(),
                                 template='flListItem')
        super(flListView, self).__init__(adapter=fl_adapter)
        fl_adapter.bind(on_selection_change=self.callback)

    def callback(self, adapter):
        if len(adapter.selection) == 0:
            print "No selected item"
        else:
            cw_name = '/'+adapter.selection[0].text
            self.datadir = self.datadir + cw_name
            print self.datadir
            self.clear_widgets()
            if self.level <= 2:
                self.__init__()
            else:
               print self
               self.add_widget(WorkingScreen())


class cwListView(ListView):

    def __init__(self, **kwargs):
        cwdata = model.data()
        cw = cwdata.Coursework()
        args_converter = \
            lambda row_index, rec: {'text': rec['text'],
                                    'is_selected': rec['is_selected'],
                                    'size_hint_y': 0.5,
                                    'height': 40}

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

class CategoryScreen1(Screen):
    pass
class CategoryScreen2(Screen):
    pass
class CategoryScreen3(Screen):
    pass

class WorkingScreen(BoxLayout):
    pass

class IseekeyApp(App):
    icon = 'image/logo1.png'
    progress = 0
    play_state = ''

    def build(self):
        root = ScreenManager()
        root.add_widget(AdScreen(name='Ad'))
        root.add_widget(SignScreen(name='sign'))
        root.add_widget(CategoryScreen1(name='category1'))
        root.add_widget(CategoryScreen3(name='category3'))
        #root.add_widget(WorkingScreen(name='working'))
        return root

    def on_start(self):
        pass

    def sign_in(self):
        pass

    def get_cw(self, screen):
        ds = DictStore('temp')
        cwd = ds.get('select_cw_desc')['desc']
        screen.current_screen.ids['cw_desc'].text = cwd

    def gsra_start(self, screen):

        r = sr.Recognizer()
        with sr.Microphone() as source:                # use the default microphone as the audio source
            audio = r.listen(source)                   # listen for the first phrase and extract it into audio data
        try:
            screen.current_screen.ids['input_speech'].text = r.recognize(audio)
        except LookupError:
            screen.current_screen.ids['input_speech'].text = ' '

    def set_cw_color(self, screen, sound, *largs):
        ds = DictStore('temp')
        cwd = ds.get('select_cw_desc')['desc']
        screen.current_screen.ids['cw_desc'].text = '[color=000000] ' + cwd + '[/color]'
        cwd_list = str.split(cwd)
        if sound.get_pos() == 0:
            progress = cwd_list.__len__()
        else:
            progress = int(round(sound.get_pos()/sound.length, 2)*cwd_list.__len__())
        cwd_list.insert(0, '[color=ff3333]')
        cwd_list.insert(progress+1, '[/color]')
        cwd_markup = ''
        for i in range(cwd_list.__len__()):
            cwd_markup = cwd_markup + cwd_list[i] + ' '
        screen.current_screen.ids['cw_desc'].text = cwd_markup

        if sound.state == 'stop':
            return False

    def load_audio(self):
        ds = DictStore('temp')
        cwf = ds.get('select_cw_file')['file']
        from kivy.core.audio import SoundLoader
        sound = SoundLoader.load('audio/'+cwf)
        return sound

    def play_origin(self, screen):
        sound = self.load_audio()
        if sound:
            sound.play()
            screen.current_screen.ids['cw_file'].text = 'Stop'
            Clock.schedule_interval(partial(self.set_cw_color, screen, sound), 0.5)
            Clock.schedule_interval(partial(self.get_progress, screen, sound), 0.5)

    def get_progress(self, screen, sound, *largs):

        self.progress = sound.get_pos()

        if self.play_state == 'replay':
            sound.stop()
            print self.progress
           # time.sleep(0.5)
            self.load_audio().play()
            print self.progress
        elif self.play_state == 'back5s':
            sound.stop()
            print self.progress
            sound.seek(self.progress)
            #sound.play()
            print sound.get_pos()
        if sound.state == 'stop':
            return False

    def play_back(self,dural):
        if self.progress > dural:
            self.progress = self.progress - dural
        else:
            self.progress = 0
        print self.progress

    def play_audio(self, state):
        self.play_state = state


if __name__ == '__main__':
    IseekeyApp().run()
