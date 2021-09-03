from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from menu import Menu
from kivy.core.window import Window
from home import Home
from picture import Picture
from results import Results

class BaseController(GridLayout):
    def __init__(self,**kwargs):
        super(BaseController,self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.menu = Menu()
        self.menuWindow = Popup(title="Menu", content=self.menu, size_hint=(.8,.8))
        self.menu.add_menu_callback(self.menu_callback)

        self.home = Home()
        #self.picture= Picture()
        self.results= Results()

        self.open_window = self.home
        self.add_widget(self.home)

        self.ignore_next= False

    def menu_callback(self,menu_item):
        self.clear_widgets()
        self.close_menu()
        if menu_item == "home":
            self.open_window = self.home
            self.add_widget(self.home)
        elif menu_item == "results":
            self.open_window = self.results
            self.add_widget(self.results)


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
                self.close_menu()
            elif (keycode[1] == 'right' or keycode[1] == 'down'):
                self.open_window.set_button_index(True)
            elif (keycode[1] == 'left' or keycode[1] == 'up'):
                self.open_window.set_button_index(False)
            elif (keycode[1] == 'lctrl'):
                self.open_window.select()

        self.ignore_next = not self.ignore_next
    
    def show_menu(self):
        self.open_window = self.menu
        self.menuWindow.open()
    def close_menu(self):
        self.menuWindow.dismiss()