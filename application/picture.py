from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty 
from interactable_page import InteractablePage
from threading import Timer

class Picture(GridLayout,InteractablePage):

    capture_button = ObjectProperty(None)
    camera = ObjectProperty(None)
    captured_label = ObjectProperty(None)

    def __init__(self,keyboard, **kwargs):
        super(Picture,self).__init__(**kwargs)

        self.button_list = [self.capture_button]

        self._keyboard = keyboard 
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

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

    def add_menu_callback(self,menu_callback):
        self.menu_callback = menu_callback

    def process_capture(self):
        print("CAPTURED")
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