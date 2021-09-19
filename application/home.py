#!/usr/bin/python3
import pandas as pd
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView 
from kivy.properties import ObjectProperty 
from interactable_page import InteractablePage
from images import Images
from kivy.core.window import Window

class Home(GridLayout,InteractablePage):

    image_view = ObjectProperty(None)
    image_name= ObjectProperty(None)
    image_button= ObjectProperty(None)
    previous_button = ObjectProperty(None)
    next_button = ObjectProperty(None)
    accuracy_label = ObjectProperty(None)

    def __init__(self,keyboard,**kwargs):

        super(Home,self).__init__(**kwargs)

        #self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard = keyboard 
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.df = pd.read_csv("/home/pi/dev/flora_dex/application/raw_data/image_paths.csv")

        ## get all unique labels and sort them (for classification_report)
        self.default_classes = list(self.df['label'].unique())
        self.default_classes.sort()

        self.classes = self.default_classes
        self.results = []

        self.use_results = False

        self.i = 0

        self.button_list = [self.image_button,self.previous_button,self.next_button]

        self.image = Images(self._keyboard)
        self.image.add_dismiss_callback(self.dismiss_callback)
        self.image_modal = ModalView()
        self.image_modal.add_widget(self.image)

        self.ignore_next = False

        self.update()


    def set_results(self,classes, accuracy):
        self.results = classes
        self.results_accuracy = accuracy
    
    def use_default_classes(self):
        self.i = 0
        self.use_results = False
        self.classes = self.default_classes
        self.accuracy_label.opacity = 0
        self.update()
    
    def use_result_classes(self):
        self.i = 0
        if (self.results == []):
            self.use_results = False
            self.classes = self.default_classes
            self.accuracy_label.opacity = 0
        else:
            self.use_results = True
            self.classes = self.results
            self.accuracy_label.opacity = 1

        self.update()

    def select(self):
        if (self.current_button.text == "View Images"):
            self.show_images()
        elif (self.current_button.text == "Previous"):
            self.show_previous()
        elif (self.current_button.text == "Next"):
            self.show_next()
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

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
    
    def dismiss_callback(self):
        self.image_modal.dismiss()
        self.has_focus = True

    def show_images(self):
        self.image.on_open()
        self.image_modal.open()
        self.has_focus = False

    def show_previous(self):
        self.i -= 1
        self.i %= len(self.classes)

        self.update()

    def show_next(self):
        self.i += 1
        self.i %= len(self.classes)

        self.update()
    
    def update(self):
        self.image_name.text = self.classes[self.i]

        if (self.use_results):
            self.accuracy_label.text = "Accuracy: " + str(int(self.results_accuracy[self.i] * 100)) + "%"

        # get all images of the current class
        self.images = self.df[self.df['label'] == self.classes[self.i]].values.tolist()

        self.image.set_images(self.images)

        self.image_view.source = self.images[0][0]