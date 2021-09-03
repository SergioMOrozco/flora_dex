from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty 
from interactable_page import InteractablePage

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