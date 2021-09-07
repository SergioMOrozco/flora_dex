import pandas as pd
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty 
from interactable_page import InteractablePage

class Home(GridLayout,InteractablePage):

    image_view = ObjectProperty(None)
    image_name= ObjectProperty(None)
    image_button= ObjectProperty(None)
    previous_button = ObjectProperty(None)
    next_button = ObjectProperty(None)

    def __init__(self,**kwargs):

        super(Home,self).__init__(**kwargs)

        self.df = pd.read_csv("clean_data/image_paths.csv")

        ## get all unique labels and sort them (for classification_report)
        self.classes = list(self.df['label'].unique())
        self.classes.sort()

        self.i = 0
        self.update()

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

        # get all images of the current class
        self.images = self.df[self.df['label'] == self.classes[self.i]].values.tolist()

        self.image_view.source = self.images[0][0]

