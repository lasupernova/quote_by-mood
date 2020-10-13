from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen 
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    
    def login(self, uname, pword):
        # load user file info into Python dict
        with open("users.json") as file:
            users = json.load(file)
        # check if username exists already
        if uname in users and users[uname]['password'] == pword:
            self.manager.transition.direction = "left"
            self.manager.current = "login_success"
        else:
            self.ids.login_failed.text = "Wrong username or password!"



class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    # add new user and info to json-users-file
    def add_user(self, uname, pword):
        # # open user.json
        with open("users.json", 'r+') as file:
            # convert json-file content to Python dict
            users = json.load(file)

        # add new user to users-dict
        users[uname] = {'username': uname, 
                            'password': pword, 
                            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
            
        # write dict with new user info back to json-file
        with open("users.json", "w") as file:
            json.dump(users, file)

        # navigate to signup success page
        self.manager.current = "sign_up_success"


class SignUpSuccess(Screen):
    def go_to_login(self): \
        # change trasnsition style (direction)
        self.manager.transition.direction = "right"
        # navigate to login page
        self.manager.current = "login_screen"


class LoginSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    
    def get_quote(self, feeling):
        # make input lowercase for latter comparison
        feeling = feeling.lower()

        # get list with path of all files in quotes-directory
        available_feelings = glob.glob("quotes\*txt")
        # get stem from each of the paths

        available_feelings = [Path(filename).stem for filename in available_feelings]
       
        # check if entered feeling exists
        if feeling in available_feelings:
            # load all quotes in file into quotes
            with open(f"quotes\\{feeling}.txt") as file:
                quotes = file.readlines()

            # select random quote
            quote = random.choice(quotes)

            # pass selected quote to Label-text
            self.ids.quote.text = quote

        else:
            # pass info that the feeling does not exist
            self.ids.quote.text = "Nope, we don't do that...choose another feeling!"


# create class with entered parents to enable specific behavior of buttons in design.kv
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class MainApp(App):
    def build(self):
        return RootWidget() #the instance (NOT the class) --> brackets


if __name__ == "__main__":
    MainApp().run()