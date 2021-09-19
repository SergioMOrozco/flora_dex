#!/usr/bin/python3
from kivy.app import App
from kivy.lang import Builder
from base_controller import BaseController

Builder.load_file("/home/pi/dev/flora_dex/application/kv_files/base.kv")
Builder.load_file("/home/pi/dev/flora_dex/application/kv_files/home.kv")
Builder.load_file("/home/pi/dev/flora_dex/application/kv_files/menu.kv")
Builder.load_file("/home/pi/dev/flora_dex/application/kv_files/picture.kv")
Builder.load_file("/home/pi/dev/flora_dex/application/kv_files/images.kv")

#Window.size = (720,480)

class MainApp(App):
    def build(self):
        return BaseController()

if __name__ == "__main__":
    MainApp().run()