from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty 
from interactable_page import InteractablePage
import time
from threading import Timer

class Picture(GridLayout,InteractablePage):

    capture_button = ObjectProperty(None)
    camera = ObjectProperty(None)
    captured_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Picture,self).__init__(**kwargs)

        self.button_list = [self.capture_button]

    def add_menu_callback(self,menu_callback):
        self.menu_callback = menu_callback

    def process_capture(self):
        camera = self.ids['camera']
        camera.export_to_png("capture.png")

        self.captured_label.opacity = 1.0

        t = Timer(3.0, self.captured_timer)
        t.start() 

    def captured_timer(self):
        self.captured_label.opacity = 0.0


        #TODO: Clean Image
        #self.menu_callback("home")

    def select(self):
        if (self.current_button.text == "Capture"):
            self.process_capture()