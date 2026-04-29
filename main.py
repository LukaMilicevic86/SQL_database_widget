
import kivy
import sqlite3
import os
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.config import Config

# set the window size:
Config.set("graphics", "width", "340")
Config.set("graphics", "width", "500")


# Mmin widget class:
class MainWid(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__()

        # add start widget to screen
        self.StartWid = StartWid()
        ST_wid = Screen(name = "Start")
        ST_wid.add_widget(self.StartWid)
        self.add_widget(ST_wid)


# start widget class:
class StartWid(BoxLayout):
    ...


# main app class and instance:
class MainApp(App):
    def build(self):
        return MainWid()
MainApp().run()