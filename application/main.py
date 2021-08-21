from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup

Builder.load_file("kv_files/main.kv")
Builder.load_file("kv_files/home.kv")
Builder.load_file("kv_files/menu.kv")
Builder.load_file("kv_files/picture.kv")
Builder.load_file("kv_files/results.kv")

class Home(GridLayout):
    pass
class Picture(FloatLayout):
    pass
class Results(GridLayout):
    pass
class Menu(FloatLayout):

    def add_menu_callback(self,menu_callback):
        self.menu_callback = menu_callback

    def show_home(self):
        self.menu_callback("home")

    def show_picture(self):
        self.menu_callback("picture")

    def show_results(self):
        self.menu_callback("results")
    pass

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

        self.add_widget(self.home,index=1)

    def menu_callback(self,menu_item):
        self.clear_widgets()
        self.close_menu()
        if menu_item == "home":
            self.add_widget(self.home)
        elif menu_item == "results":
            self.add_widget(self.results)


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode[1])
        if keycode[1] == 'enter':
            self.show_menu()
        if keycode[1] == 'alt':
            self.close_menu()
    
    def show_menu(self):
        self.menuWindow.open()
    def close_menu(self):
        self.menuWindow.dismiss()

class MainApp(App):
    def build(self):
        return main_kv()

if __name__ == "__main__":

    MainApp().run()