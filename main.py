__author__ = 'isaacjiang'

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from views import FView,WView
from functions import PasswordCheck


class AScreen(Screen):
    pass


class SScreen(Screen):
    pass


class CScreen(Screen):
    pass


class IseekeyApp(App):
    icon = 'image/logo1.png'

    def build(self):
        root = ScreenManager()
        root.add_widget(AScreen(name='ad'))
        root.add_widget(SScreen(name='sign'))
        root.add_widget(CScreen(name='main'))
        return root

    def on_start(self):
        pass

    def sign_in(self):
        pwcheck = PasswordCheck()
        pwcheck.check_password()

if __name__ == '__main__':
    IseekeyApp().run()
