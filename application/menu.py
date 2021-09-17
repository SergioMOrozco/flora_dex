from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty 
from interactable_page import InteractablePage

class Menu(FloatLayout, InteractablePage):

    home_button = ObjectProperty(None)
    camera_button = ObjectProperty(None)
    results_button = ObjectProperty(None)

    def __init__(self,keyboard,**kwargs):
        super(Menu,self).__init__(**kwargs)

        self._keyboard = keyboard 
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.button_list = [self.home_button,self.camera_button,self.results_button]

        self.has_focus = False

    def add_menu_callback(self,menu_callback):
        self.menu_callback = menu_callback

    def show_home(self):
        self.menu_callback("home")

    def show_picture(self):
        self.menu_callback("picture")

    def show_results(self):
        self.menu_callback("results")

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # double press on gamepad for whatever reason
        if (not self.ignore_next and self.has_focus):
            if (keycode[1] == 'right' or keycode[1] == 'down'):
                self.set_button_index(True)
            elif (keycode[1] == 'left' or keycode[1] == 'up'):
                self.set_button_index(False)
            elif (keycode[1] == 'lctrl'):
                self.select()

        self.ignore_next = not self.ignore_next
    
    def select(self):
        if (self.current_button.text == "Home"):
            self.show_home()
        elif (self.current_button.text == "Camera"):
            self.show_picture()
        elif (self.current_button.text == "Results"):
            self.show_results()