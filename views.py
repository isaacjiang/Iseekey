__author__ = 'isaacjiang'

from kivy.uix.listview import ListView
from kivy.uix.boxlayout import BoxLayout
from kivy.adapters.dictadapter import DictAdapter
from kivy.storage.jsonstore import JsonStore
from functions import PlayAudio, SpeechInput,Grading
import os


class FView(ListView):
    datadir = os.getcwd()+'/data'
    level = 0

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
        f_adapter = DictAdapter(data=subdirs,
                                 args_converter=args_converter,
                                 sorted_keys=subdirs.keys(),
                                 template='FListItem')
        super(FView, self).__init__(adapter=f_adapter)
        f_adapter.bind(on_selection_change=self.callback)

    def callback(self, adapter):
        if len(adapter.selection) == 0:
            print "No selected item"
        else:
            cw_name = adapter.selection[0].text
            self.datadir = self.datadir +'/'+ cw_name
            self.clear_widgets()
            if self.level <= 2:
                self.__init__()
            else:
                self.add_widget(WView(self.datadir))


class WView(BoxLayout):

    def __init__(self, dir):
        self.selected_filename = dir
        super(WView, self).__init__()
        self.read_data_descript()

    def play_audio(self, Flag):
        if Flag == 1:
            self.player = PlayAudio(kwargs={'filename': self.selected_filename,'root': self})
            self.player.start()

        elif Flag == 0:
            print Flag
            self.player.stop()
        else:
            print Flag
            self.player.playback(Flag)

    def gsra_start(self):
        gsra = SpeechInput(args=self)
        gsra.start()

    def read_data_descript(self):
        filename = self.selected_filename
        descript = JsonStore('data_descript.json')
        desc = descript.get(filename)['desc']
        self.ids['cw_desc'].text = desc

    def grade(self):
        grading = Grading()
        marks = grading.get_grade(self.selected_filename, self)
        self.ids['marks'].text = 'Congratuactions! Your mark is %d '%marks
        print marks