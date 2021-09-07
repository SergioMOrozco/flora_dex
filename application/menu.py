from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty 
from interactable_page import InteractablePage

class Menu(FloatLayout, InteractablePage):

    home_button = ObjectProperty(None)
    camera_button = ObjectProperty(None)
    results_button = ObjectProperty(None)

    def __init__(self,**kwargs):

        super(Menu,self).__init__(**kwargs)

        self.button_list = [self.home_button,self.camera_button,self.results_button]

    def add_menu_callback(self,menu_callback):
        self.menu_callback = menu_callback

    def show_home(self):
        self.menu_callback("home")

    def show_picture(self):
        self.menu_callback("picture")

    def show_results(self):
        self.menu_callback("results")
    
    def select(self):
        if (self.current_button.text == "Home"):
            self.show_home()
        elif (self.current_button.text == "Camera"):
            self.show_picture()
        elif (self.current_button.text == "Results"):
            self.show_results()