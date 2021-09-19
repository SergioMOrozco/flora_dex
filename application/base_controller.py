#!/usr/bin/python3
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from menu import Menu
from kivy.core.window import Window
from home import Home
from picture import Picture

class BaseController(GridLayout):

    def __init__(self,**kwargs):
        super(BaseController,self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.menu = Menu(self._keyboard)
        self.menuWindow = Popup(title="Menu", content=self.menu, size_hint=(.8,.8))
        self.menu.add_menu_callback(self.menu_callback)

        self.home = Home(self._keyboard)
        self.picture= Picture(self._keyboard)
        self.picture.add_picture_callback(self.picture_callback)

        self.open_window = self.home
        self.prev_window = self.open_window
        self.open_window.has_focus = True
        self.add_widget(self.home)

        self.ignore_next= True
        self.menu_open = False

    def menu_callback(self,menu_item):
        self.clear_widgets()
        self.close_menu()
        if menu_item == "home":
            self.open_window = self.home
            self.home.use_default_classes()
            self.add_widget(self.home)
        elif menu_item == "picture":
            self.open_window = self.picture
            self.add_widget(self.picture)
        elif menu_item == "results":
            self.open_window = self.home
            self.home.use_result_classes()
            self.add_widget(self.home)

        # sometimes the user wont close the image modal before hand
        self.home.image_modal.dismiss()
        self.open_window.ignore_next = True
        self.open_window.has_focus = True
    
    def picture_callback(self,classes,accuracy):
        self.home.set_results(classes,accuracy)


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):

        # double press on gamepad for whatever reason
        if (not self.ignore_next):
            print(keycode[1])
            if keycode[1] == 'enter':
                self.show_menu()
            elif keycode[1] == 'alt':
                if (self.menu_open):
                    self.open_window = self.prev_window
                    self.open_window.has_focus = True
                self.close_menu()

        self.ignore_next = not self.ignore_next
    
    def show_menu(self):
        if (not self.menu_open):
            self.open_window.has_focus = False
            self.prev_window = self.open_window

            self.open_window = self.menu
            self.open_window.has_focus = True
            self.menuWindow.open()
            self.menu_open = True

    def close_menu(self):
        if (self.menu_open):
            self.open_window.has_focus = False

            self.menuWindow.dismiss()
            self.menu_open = False