
import kivy
import sqlite3
import os
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.config import Config

# set the default window size:
Config.set("graphics", "width", "340")
Config.set("graphics", "width", "500")


# connect to database function
def connect_to_database(path):
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        create_table_products(cursor)
        con.commit()
        con.close()
    except Exception as e:
        print(e)

# create database table using SQL syntax
def create_table_products(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products(
            ID          INTEGER     PRIMARY KEY     AUTOINCREMENT,
            Name        TEXT        NOT NULL,
            Code        TEXT        NOT NULL,
            Price       FLOAT       NOT NULL,
            Quantity    INT         NOT NULL
        )
        """
    )


# Mmin widget class:
class MainWid(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__()

        self.APP_PATH = os.getcwd()
        self.DB_PATH = self.APP_PATH + "/my_database.db"

        # add start widget to screen
        self.StartWid = StartWid(self)
        ST_wid = Screen(name = "Start")
        ST_wid.add_widget(self.StartWid)
        self.add_widget(ST_wid)

        # add database widget to screen
        self.DataBaseWid = DataBaseWid(self)
        DB_wid = Screen(name = "Database")
        DB_wid.add_widget(self.DataBaseWid)
        self.add_widget(DB_wid)

        self.go_to_start()

    # open the start widget as current screen

    def go_to_start(self):
        self.current = "Start"

    # open the database widget as current screen

    def go_to_database(self):
        self.DataBaseWid.check_memory()
        self.current = "Database"




# start widget class:
class StartWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super().__init__()
        self.mainwid = mainwid

    # method to create the database using the path from the mainwid
    def create_database(self):
        connect_to_database(self.mainwid.DB_PATH) 
        self.mainwid.go_to_database()


# database widget class:    
class DataBaseWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super().__init__()
        self.mainwid = mainwid
    
    # method to delete everything from screen and add everything that is present in the database

    def check_memory(self):
        self.ids.container.clear_widgets()

        wid = NewDataButton(self.mainwid)
        self.ids.container.add_widget(wid)



# product entry button:
class NewDataButton(Button):
    def __init__(self, mainwid, **kwargs):
        super().__init__()
        self.mainwid = mainwid

    def create_new_product(self):
        print("Product to be added")


# main app class and instance:
class MainApp(App):
    def build(self):
        return MainWid()
MainApp().run()