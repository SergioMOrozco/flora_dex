#!/usr/bin/python3
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.floatlayout import FloatLayout
from interactable_page import InteractablePage
from kivy.properties import ObjectProperty 

class Images(FloatLayout,InteractablePage):

    image_view = ObjectProperty(None)
    previous_button = ObjectProperty(None)
    next_button = ObjectProperty(None)

    def __init__(self,keyboard,**kwargs):
        super(Images,self).__init__(**kwargs)

        self._keyboard = keyboard
        self.images = []
        self.i = 0
        self.button_list = [self.previous_button,self.next_button]
        self.ignore_next= True

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # double press on gamepad for whatever reason
        if (not self.ignore_next and self.has_focus):
            if (keycode[1] == 'right' or keycode[1] == 'down'):
                self.set_button_index(True)
            elif (keycode[1] == 'left' or keycode[1] == 'up'):
                self.set_button_index(False)
            elif (keycode[1] == 'lctrl'):
                self.select()
            elif keycode[1] == 'alt':
                self.dismiss()

        self.ignore_next = not self.ignore_next
    
    def add_dismiss_callback(self,dismiss_callback):
        self.dismiss_callback = dismiss_callback
    
    def dismiss(self):
        self.has_focus = False
        self.dismiss_callback()
        

    def set_images(self,images):
        self.images = images
        self.image_view.source = self.images[0][0]

    def select(self):
        if (self.current_button.text == "Previous"):
            self.show_previous()
        elif (self.current_button.text == "Next"):
            self.show_next()

    def show_previous(self):
        self.i -= 1
        self.i %= len(self.images)

        self.update()

    def show_next(self):
        self.i += 1
        self.i %= len(self.images)

        self.update()

    def update(self):
        self.image_view.source = self.images[self.i][0]
    def on_open(self):
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.has_focus = True



