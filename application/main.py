from kivy.app import App
from kivy.lang import Builder
from base_controller import BaseController

Builder.load_file("kv_files/base.kv")
Builder.load_file("kv_files/home.kv")
Builder.load_file("kv_files/menu.kv")
Builder.load_file("kv_files/picture.kv")
Builder.load_file("kv_files/results.kv")

class MainApp(App):
    def build(self):
        return BaseController()

if __name__ == "__main__":
    MainApp().run()