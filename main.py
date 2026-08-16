
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


# connect to database function, called by the create database function
def connect_to_database(path):
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        create_table_products(cursor)
        con.commit()
        con.close()
    except Exception as e:
        print(e)

# create database table using SQL syntax; called upon pressing tthe create/enter button in Start widget
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

        # add start widget to screen and screen to screen manager
        self.StartWid = StartWid(self)
        ST_wid = Screen(name = "Start")
        ST_wid.add_widget(self.StartWid)
        self.add_widget(ST_wid)

        # add database widget to screen and screen to screen manager
        self.DataBaseWid = DataBaseWid(self)
        DB_wid = Screen(name = "Database")
        DB_wid.add_widget(self.DataBaseWid)
        self.add_widget(DB_wid)

        # add insert data widget to screen and screen to screen manager
        self.InsertDataWid = InsertDataWid(self)
        IDW_wid = Screen(name = "InsertData")
        IDW_wid.add_widget(self.InsertDataWid)
        self.add_widget(IDW_wid)

        self.go_to_start()

    # open the start widget as current screen
    def go_to_start(self):
        self.current = "Start"

    # open the database widget as current screenA
    def go_to_database(self):
        self.DataBaseWid.check_memory()
        self.current = "Database"

    #reset everything in insert data widget and open that screen
    def go_to_insertdata(self):
        self.InsertDataWid.clear_widgets() #clears everything from last time
        NewInsertDataWid = InsertDataWid(self)
        self.InsertDataWid.add_widget(NewInsertDataWid)
        self.current  = "InsertData"


# start widget class:
class StartWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super().__init__()
        self.mainwid = mainwid

    # method to create the database using the path from the mainwid, called when the startwid button is pressed
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

        NDBwid = NewDataButton(self.mainwid) 
        self.ids.container.add_widget(NDBwid)



# product entry button:
class NewDataButton(Button):
    def __init__(self, mainwid, **kwargs):
        super().__init__()
        self.mainwid = mainwid

    def create_new_product(self):
        self.mainwid.go_to_insertdata() 

# widget to create new product and fill the data in the table columns
class InsertDataWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super().__init__()
        self.mainwid = mainwid

    #method to fill in the data windows for columns in the table
    def insert_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()

        d1 = self.ids.ti_name.text
        d2 = self.ids.ti_code.text
        d3 = self.ids.ti_price.text
        d4 = self.ids.ti_quantity.text
        

        a1 = (d1, d2, d3, d4)

        s1 = 'INSERT INTO products(Name,Code,Price,Quantity)'
        s2 = 'VALUES("%s", "%s", %s, %s)' %a1 # %s are placeholders for strings and numbers

        try:
            cursor.execute(s1 + " " + s2)
            con.commit()
            con.close()
            self.mainwid.go_to_database()

        except Exception as e:
            print(str(e))
            #message = self.mainwid.Popup.ids.message
            #self.mainwid.Popup.open()
            #self.mainwid.Popup.title = "Error!"
            #if "" in a1:
             #   message.text = "One or more fields empty"
            #else:
             #   message.text = str(e)

    #return to the database widget upon pressing Exit
    def back_to_dbw(self):
        self.mainwid.go_to_database()


# main app class and instance:
class MainApp(App):
    def build(self):
        return MainWid()
MainApp().run()