
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

        # add update data widget to screen and screen to screen manager
        self.UpdateDataWid = UpdateDataWid(self, data_id = '0') #set to 0 as initial value since ID ise expected in the argument after clicking Edit button
        UDW_wid = Screen(name = "UpdateData")
        UDW_wid.add_widget(self.UpdateDataWid)
        self.add_widget(UDW_wid)

        self.Popup = MessagePopup()
 
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

    #reset everything in update data widget and open that screen
    def go_to_updatedata(self, data_id):
        self.UpdateDataWid.clear_widgets()
        UDW_wid = UpdateDataWid(self, data_id)
        self.UpdateDataWid.add_widget(UDW_wid)
        self.current = "UpdateData"
    


# 1st screen, start widget class:
class StartWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super().__init__()
        self.mainwid = mainwid

    # method to create the database using the path from the mainwid, called when the startwid button is pressed
    def create_database(self):
        connect_to_database(self.mainwid.DB_PATH) 
        self.mainwid.go_to_database()


# 2nd screen, database widget class:    
class DataBaseWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
        super().__init__()
        self.mainwid = mainwid
    
    # method to delete everything from screen and add everything that is present in the database
    def check_memory(self):
        self.ids.container.clear_widgets()

        con = sqlite3.connect(self.mainwid.DB_PATH) #connect to database
        cursor = con.cursor()
        # SQL command for cursor to select all columns intable, row by row:
        cursor.execute(
            'SELECT ID, Name, Code, Price, Quantity FROM products'
        )
        for element in cursor: # element is each row
            Dwid = DataWid(self.mainwid)
            r1 = "ID: " + str(element[0]) + "\n" #element zero is ID
            r2 = element[1] + "\n"
            r3 = "Code: " + element[2] + "\n"
            r4 = "Price: " + str(element[3]) + "\n"
            r5 = "Quantity: " + str(element[4]) + "\n"
            Dwid.data_id = str(element[0]) #connects the primary key from the table to an ID to be used for editing
            Dwid.data = r1 + r2 + r3 + r4 + r5
            self.ids.container.add_widget(Dwid)

        NDBwid = NewDataButton(self.mainwid) 
        self.ids.container.add_widget(NDBwid)
        con.close()


# product entry button:
class NewDataButton(Button):
    def __init__(self, mainwid, **kwargs):
        super().__init__()
        self.mainwid = mainwid

    def create_new_product(self):
        self.mainwid.go_to_insertdata() 

# class for the message popup window:
class MessagePopup(Popup):
    ...

# class for widgets to populate 2nd screen upon  inserting data in the 3d
class DataWid(BoxLayout):
    def __init__(self, mainwid, **kwargs):
            super().__init__()
            self.mainwid = mainwid
    def open_update_data(self, data_id):
        self.mainwid.go_to_updatedata(data_id)
# 3rd screen, widget to create new product and fill the data in the table columns
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

        s1 = 'INSERT INTO products (Name, Code, Price, Quantity)'
        s2 = 'VALUES("%s", "%s", %s, %s)' %a1 # %s are SQL placeholders for strings and numbers from the python code, after the %

        try:
            cursor.execute(s1 + " " + s2)
            con.commit()
            con.close()
            self.mainwid.go_to_database()

        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Error!"
            if "" in a1:
               message.text = "One or more fields empty"
            else:
               message.text = str(e)

    #return to the database widget upon pressing Exit
    def back_to_dbw(self):
        self.mainwid.go_to_database()

# 4th screen for editing the entries from the Database Widger
class UpdateDataWid(BoxLayout):
    def __init__(self, mainwid, data_id, **kwargs):
        super().__init__()
        self.mainwid = mainwid
        self.data_id = data_id
        self.check_updatedata_memory()

    def check_updatedata_memory(self):

        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()

        # SQL command for cursor to select all columns in table in row with corresponding primary key:
        s = 'SELECT Name, Code, Price, Quantity FROM products WHERE ID = '

        cursor.execute(s + self.data_id)

        for element in cursor: # element is each row
            self.ids.ti_name.text = str(element[0])
            self.ids.ti_code.text = str(element[1])
            self.ids.ti_price.text = str(element[2])
            self.ids.ti_quantity.text = str(element[3])

        con.close()

    def update_data(self):
        con = sqlite3.connect(self.mainwid.DB_PATH)
        cursor = con.cursor()

        d1 = self.ids.ti_name.text
        d2 = self.ids.ti_code.text
        d3 = self.ids.ti_price.text
        d4 = self.ids.ti_quantity.text
        

        a1 = (d1, d2, d3, d4)

        # SQL syntax for cursor to update each column with elements from a1 through placeholders
        s1 = 'UPDATE products SET'
        s2 = 'Name = "%s", Code = "%s", Price = %s, Quantity = %s' %a1   
        s3 = 'WHERE ID = %s' %self.data_id

        cursor.execute(s1 + " " + s2 + " " + s3)
        con.commit()
        con.close()
        self.mainwid.go_to_database()
    
                
    def delete_data(self):
        ...

    def back_to_dbw(self):
        self.mainwid.go_to_database()

# main app class and instance:
class MainApp(App):
    def build(self):
        return MainWid()
MainApp().run()