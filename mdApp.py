import os, sys
import datetime     #FOR date saving of current date
import base64       #FOR password encoding

from kivy.lang import Builder
from kivy.config import Config
Config.set('graphics', 'width', '600')   #change screen width
Config.set('graphics', 'height', '800')  #change screen height

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton,MDFillRoundFlatButton
from kivymd.uix.screenmanager import MDScreenManager
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.resources import resource_add_path, resource_find
from kivymd.uix.dialog import MDDialog
import sqlite3
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.snackbar import Snackbar
from kivy.core.window import Window
from kivymd.uix.snackbar import BaseSnackbar
from kivymd.uix.card import MDCard 
import io
from kivy.core.image import Image as CoreImage
from kivymd.uix.list import ThreeLineListItem
from datetime import timedelta


class CustomSnackbar(BaseSnackbar):
    text        = StringProperty(None)
    icon        = StringProperty(None)
    font_size   = NumericProperty("15sp")

class CustomCard(MDCard):
    id      = StringProperty(None)
    title   = StringProperty(None)
    source  = StringProperty(None)
    group   = StringProperty(None)
    def assign_texture_from_database(self, dbTexture):
        self.ids.display_image.texture = dbTexture
        

#Builder.load_file('./mdAppComponents.kv')    
class MainLayout(BoxLayout):
    def datetime_difference(self, from_date):
        decimal_index = from_date.find('.')
        if decimal_index != -1:
            from_date = from_date[:decimal_index]
        now = datetime.datetime.now()
        try:
            record_date = datetime.datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        except:
            print(f"error from date {from_date}")
            
        record_date = datetime.datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        
        diff = now - record_date
        if diff < timedelta(minutes = 60):
            return f"{int(diff.seconds / 60)}m"
        elif diff < timedelta(days = 1):
            return f"{int(diff.seconds / 36000)}h"
        elif diff < timedelta(days = 30):
            return f"{diff.days}d"
        else:
            return f"{int(diff.days / 30)}mo"
        
        
    
    def load_posts(self):
        self.dbconn = sqlite3.connect('C:/Users/Student/Desktop/Kivy Dev/kivy-venv/Codes/Slide 10/kivysql2.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = self.dbconn.cursor()
        dbcursor.execute("SELECT * FROM trnpost  ORDER BY trnpost.created_at DESC")
        records = dbcursor.fetchall()
        if not records:
            print("no records")
        else:
            self.ids.screen4_boxlayout.clear_widgets()
            for post in records:
                self.ids.screen4_boxlayout.add_widget(ThreeLineListItem(text=f'[size=18sp][b]{post[2]}[/b][/size]',
                                                                        secondary_text=f'[size=12sp]posted by: {post[5]} {self.datetime_difference(post[7])}[/size]',
                                                                        tertiary_text=post[3]))
            

        
    """def check_user(self, input_rarity):
        self.dbconn = sqlite3.connect('C:/Users/Student/Desktop/Kivy Dev/kivy-venv/Codes/Slide 10/kivysql2.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = self.dbconn.cursor()
        dbcursor.execute(
            "SELECT * FROM mstimages WHERE mstimages.rarity = :var_rarity",
            {
                'var_rarity' : input_rarity
            })
        if input_rarity == 5:
            self.ids."""
    def load_cards(self):
        
        """self.ids.screen1_grid.clear_widgets()
        mdCard = CustomCard(id="1", title="Test", source=f"", group="group")
        self.ids.screen1_grid.add_widget(mdCard)
        mdCard2 = CustomCard(id="2", title="Test2", source=f"", group="group2")
        self.ids.screen1_grid.add_widget(mdCard2)"""
        self.dbconn = sqlite3.connect('C:/Users/Student/Desktop/Kivy Dev/kivy-venv/Codes/Slide 10/kivysql2.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = self.dbconn.cursor()
        dbcursor.execute("SELECT * FROM mstimages ORDER BY mstimages.code")
        records = dbcursor.fetchall()
        if not records:
            print("No Records Detected")
            return False
        else:
            self.ids.screen1_grid.clear_widgets()
            for img_rec in records:
                mdCard = CustomCard(id = str(img_rec[0]), 
                                    title = img_rec[1], 
                                    source= f"", 
                                    group= img_rec[2])
                if img_rec[4] == 5:
                    mdCard.md_bg_color = "DCA454"
                else:
                    mdCard.md_bg_color = "9174A9"
                
                data = io.BytesIO(img_rec[3])
                dbImage = CoreImage(data, ext="webp").texture
                mdCard.assign_texture_from_database(dbImage)
                self.ids.screen1_grid.add_widget(mdCard)
        self.dbconn.commit()
        self.dbconn.close()
                
    
    def open_icon_snackbar(self):
        snackbar = CustomSnackbar(
            text="This is a sample snackbar error!",
            icon= "close-circle",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x= (Window.width - (dp(10) * 2)) / Window.width,
            bg_color="#B71C1C")
        snackbar.open()
    
    def open_custom_snackbar(self):
        snackbar = Snackbar(text = "Yo! This is a custom snackbar!", 
                            font_size = '16dp', bg_color = "orange", 
                            snackbar_x = "10dp", snackbar_y = "10dp",
                            size_hint_x = (Window.width - (dp(10) * 2)) / Window.width)
        snackbar.open()
        
    store = JsonStore("loggedUser.json")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.store = JsonStore("loggedUser.json")
        try:
            if self.store.get('UserInfo')['firstname'] != "":
                self.screen_manager.current = 'dashboard_screen'
        except KeyError:
            self.screen_manager.current = 'login_screen'
        
        self.load_cards()
        
        
    screen_manager = ObjectProperty(None)
    dbconn    = None
    dialogbox = None
    
    def check_user(self, input_username, input_password):
        self.dbconn = sqlite3.connect('C:/Users/Student/Desktop/Kivy Dev/kivy-venv/Codes/Slide 10/kivysql.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = self.dbconn.cursor()
        dbcursor.execute(
            "SELECT * FROM mstuser WHERE mstuser.username = :var_username and mstuser.password = :var_password",
            {
                'var_username' : input_username,
                'var_password' : self.password_encode(input_password)
            })
        records = dbcursor.fetchall()
        
        if not records:
            print("No Records Detected")
            return False
        else:
            for user in records:
                print(f"Username:{user[1]}\nFirstName:{user[2]}\nLastName:{user[3]}")
                self.store.put('UserInfo',code=user[0],firstname=user[2],lastname=user[3],username=user[1])
            self.dbconn.commit()
            self.dbconn.close()
            self.ids.screen_manager1.current = "dashboard_screen"
            self.ids.screen_manager1.transition.direction = "up"
            return True
        
    
    def login_account(self):
        """
        Validate username and password from user input. If the value of login_complete
        is true, generate a Login Success dialogbox, otherwise, prompt that username and password 
        not found.
        """
        
        input_username = self.ids.log_username.text.strip()
        input_password = self.ids.log_password.pass_text.text.strip()
        login_complete = self.check_user(input_username, input_password)  
        if login_complete: 
            self.display_dialog("Login Success!")
        else:
            self.display_dialog("Username & password not found")
    
    def add_user(self):
        self.dbconn = sqlite3.connect('C:/Users/Student/Desktop/Kivy Dev/kivy-venv/Codes/Slide 10/kivysql.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = self.dbconn.cursor()
        dbcursor.execute(
            "INSERT INTO mstuser (username, first_name, last_name, email, password, created_at, updated_at) VALUES (:var_username, :var_firstname, :var_lastname, :var_email, :var_password, :var_created_at, :var_updated_at)", 
            {
                'var_username' : self.ids.username.text.strip(),
                'var_firstname' : self.ids.firstname.text.strip(),
                'var_lastname' : self.ids.lastname.text.strip(),
                'var_email' : self.ids.email.text.strip(),
                'var_password' : self.password_encode(self.ids.password.pass_text.text.strip()),
                'var_created_at' : datetime.datetime.now(),
                'var_updated_at' : datetime.datetime.now(),
            })
        if(dbcursor.rowcount < 1):
            print("No Record Created")
            return False
            
        else:
            print("Record Inserted")
            self.dbconn.commit()
            self.dbconn.close()
            return True
        
    def register_account(self,app):
        """
        Validate registration fields using input_validate function. If the value of reg_complete
        is true, generate a Registration Success dialogbox, otherwise, prompt that an error message.
        """
        
        if self.input_validate():
            reg_complete = self.add_user() #insert record to database
            if reg_complete: 
                self.display_dialog("", True)
            else:
                self.display_dialog("Error inserting records")
           
            
            
    def display_dialog(self, text_msg,is_success=False):
        """
        Use to generate dialog box with parameter-based text property. If is_success is true,
        generate a customize dialog box for registration success prompt

            Parameter:
                text_msg(str)   : Message to display in dialog box
                is_success(bool): Default to False, if this is true, display a custom success
                                  dialogbox 
        """
        
        if is_success :
            self.dialogbox = None
            if not self.dialogbox:
                self.clear_registration()
                self.dialogbox = MDDialog(
                    type="custom",
                    content_cls=RegDialogContent(),
                    buttons = [MDFillRoundFlatButton(
                                    text='Return to Login',  #pad blank spaces left and right
                                    font_size="20sp",
                                    md_bg_color="orange",
                                    pos_hint={'center_x': 0.5},
                                    on_release=self.reg_success_ok_button
                                )],
                )
            self.dialogbox.open()  
        else:
            self.dialogbox = None
            if not self.dialogbox:
                self.dialogbox = MDDialog(
                    text=f"[color=#263238]{text_msg}[/color]",
                    buttons = [MDRaisedButton(
                            text="Ok",
                            md_bg_color="orange",
                            pos_hint={'center_x': 0.5},
                            on_press=self.dismiss_dialog)],
                )
            self.dialogbox.open()  
        
    
        
    def dismiss_dialog(self,*args):
        """
        Function to close/dismiss the current dialogbox
        """
        
        if self.dialogbox: #requires to have an existing dialogbox open
            self.dialogbox.dismiss()
    
    
    
    def reg_success_ok_button(self,*args):
        """
        A dismiss_dialog() copy, specific to registration success dialog box.
        Dismiss the dialog box and return to login screen after pressing the
        'Return to Login' button
        """
        
        if self.dialogbox: #requires to have an existing dialogbox open
            self.dismiss_dialog()
            self.screen_manager.current = "login_screen" 
            self.screen_manager.transition.direction = "right"     
        
    
           
    def input_validate(self):
        """
        Validate user input in registration screen. Returns True if all validations are passed.
        
            Returns:
                True/False(bool): 
        """
        
        #strip removes any extra spaces
        username    = self.ids.username.text.strip()  
        firstname   = self.ids.firstname.text.strip()  
        lastname    = self.ids.lastname.text.strip()  
        email       = self.ids.email.text.strip()  
        password    = self.ids.password.pass_text.text.strip()
        cbTerms     = self.ids.checkBox.active
        
        #check if any one of the fields is empty
        if not username or not firstname or not lastname or not email or not password: 
            self.display_dialog("Please fill up all required fields") 
            return False    
        #check if checkbox is not checked   
        elif not cbTerms:
            self.display_dialog("You must agree to terms and condition")
            return False
        else:
            return True   
            
    
            
    def password_encode(self,password_string):
        """
        Encode password into b64 encryption for database storage.
        
            Returns:
                password(string): encoded password in b64encoding 
        """
        
        ascii_pass  = password_string.encode("ascii")
        b64_pass    = base64.b64encode(ascii_pass)
        return b64_pass.decode("ascii")
    
    
    
    def password_decode(self,password_string):
        """
        Decode password into b64 decryption for password viewing(not in use in this app).
        
            Returns:
                password(string): decoded password
        """
        
        ascii_pass  = password_string.encode("ascii")
        b64_pass    = base64.b64decode(ascii_pass)
        return b64_pass.decode("ascii")
    
    
    
    def clear_registration(self):
        """
        Clear input fields in registration screen.
        """
        self.ids.username.text  = ''
        self.ids.firstname.text = ''
        self.ids.lastname.text  = ''
        self.ids.email.text     = ''
        self.ids.password.pass_text.text = ''
        self.ids.checkBox.active = False

        
class CustomPasswordField(MDRelativeLayout):
    text      = StringProperty()
    hint_text = StringProperty()
    pass_text = ObjectProperty(None)

class CustomPasswordRegField(MDRelativeLayout):
    text      = StringProperty()
    hint_text = StringProperty()      
    pass_text = ObjectProperty(None)

class RegDialogContent(MDBoxLayout):
    pass      

class mdAppComponentsApp(MDApp):
    def build(self):
            self.theme_cls.material_style = "M3"    
            self.theme_cls.theme_style    = "Light"
            self.theme_cls.primary_palette= "Blue"
            self.theme_cls.accent_palette = "Teal"
            return MainLayout()  
        
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    mdAppComponentsApp().run()