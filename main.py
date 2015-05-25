from kivy.app import App
import kivy.properties as prop
from kivy.uix.screenmanager import ScreenManager

import functions

class ScreenManager(ScreenManager):

    username_prop = prop.ObjectProperty()

class ISeeKeyApp(App):
    icon = 'image/logo1.png'

    def build(self):

        print(self.root.children)

    def sign_in(self):
        self.root.username_prop.text = 'Hello'

    def on_start(self):
        pass

if __name__ == '__main__':
    ISeeKeyApp().run()

