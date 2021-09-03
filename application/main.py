from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty 
from kivy.uix.popup import Popup
from kivy.graphics import Color

Builder.load_file("kv_files/base.kv")
Builder.load_file("kv_files/home.kv")
Builder.load_file("kv_files/menu.kv")
Builder.load_file("kv_files/picture.kv")
Builder.load_file("kv_files/results.kv")

class InteractablePage:

    def __init__(self):
        self.button_list = []
        self.button_index = -1

    def set_button_index(self,increment):
        if len(self.button_list) == 0:
            return 

        if increment:
            self.button_index +=1
        else:
            self.button_index -=1

        self.button_index = self.button_index % len(self.button_list)
        self.current_button = self.button_list[self.button_index]

        if increment:
            previous_button = self.button_list[(self.button_index -1 + 3) % len(self.button_list)]
        else:
            previous_button = self.button_list[(self.button_index + 1 + 3) % len(self.button_list)]

        previous_button.background_color = (0,0,0,0)
        self.current_button.background_color = (1,1,1,1)
        self.current_button.color = (0,0,0,1)

    
    def select(self):
        pass
    
    def deselect(self):
        pass

class Home(GridLayout,InteractablePage):
    image_button= ObjectProperty(None)
    previous_button = ObjectProperty(None)
    next_button = ObjectProperty(None)

    def __init__(self,**kwargs):

        super(Home,self).__init__(**kwargs)

        self.button_list = [self.image_button,self.previous_button,self.next_button]

    def select(self):
        if (self.current_button.text == "View Images"):
            self.show_images()
        elif (self.current_button.text == "Previous"):
            self.show_next()
        elif (self.current_button.text == "Next"):
            self.show_previous()

    def show_images(self):
        print("show images")

    def show_picture(self):
        print("show previous")

    def show_results(self):
        print("show next")

class Picture(FloatLayout):
    pass
class Results(GridLayout):
    pass

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
            self.show_home()
        elif (self.current_button.text == "Results"):
            self.show_results()

class main_kv(GridLayout):
    def __init__(self,**kwargs):
        super(main_kv,self).__init__(**kwargs)

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

class MainApp(App):
    def build(self):
        return main_kv()

if __name__ == "__main__":
    MainApp().run()