from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

Builder.load_file("kv_files/main.kv")
Builder.load_file("kv_files/home.kv")
Builder.load_file("kv_files/picture.kv")
Builder.load_file("kv_files/results.kv")

#class MyGrid(Widget):
#    name = ObjectProperty(None)
#    email = ObjectProperty(None)
#
#    def btn(self):
#        print("Name:",self.name.text,"Email:",self.email.text)


#class MyGrid(GridLayout):
#    def __init__(self, **kwargs):
#
#        super(MyGrid, self).__init__(**kwargs)
#
#        self.inside = GridLayout()
#        self.inside.cols = 2
#        
#
#        self.cols = 1
#        self.f_name = TextInput(multiline=False)
#        self.l_name = TextInput(multiline=False)
#        self.submit = Button(text="Submit", font_size=40)
#        self.submit.bind(on_press=self.pressed)
#
#        self.inside.add_widget(Label(text="First Name: "))
#        self.inside.add_widget(self.f_name)
#        self.inside.add_widget(Label(text="Last Name: "))
#        self.inside.add_widget(self.l_name)
#
#        self.add_widget(self.inside)
#        self.add_widget(self.submit)
#
#    def pressed(self,instance):
#        print("pressed")

class Home(GridLayout):
    pass
class Picture(GridLayout):
    pass
class Results(GridLayout):
    pass

class main_kv(GridLayout):
    def __init__(self,**kwargs):

        super(main_kv,self).__init__(**kwargs)

        self.home = Home()
        self.picture= Picture()
        self.results= Results()

        self.add_widget(self.home,index=1)

    def show_home(self):
        self.clear_tabs()
        self.add_widget(self.home,index=1)

    def show_picture(self):
        self.clear_tabs()
        self.add_widget(self.picture,index=1)

    def show_results(self):
        self.clear_tabs()
        self.add_widget(self.results,index=1)

    def clear_tabs(self):
        self.remove_widget(self.home)
        self.remove_widget(self.picture)
        self.remove_widget(self.results)



    pass

class MainApp(App):
    def build(self):
        #return MyGrid()
        return main_kv()

if __name__ == "__main__":
    MainApp().run()