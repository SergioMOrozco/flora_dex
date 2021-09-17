class InteractablePage:

    def __init__(self):
        self.button_list = []
        self.button_index = -1
        self.has_focus = False
        self.ignore_next = False

    def set_button_index(self,increment):
        if len(self.button_list) == 0:
            return 

        if increment:
            self.button_index +=1
        else:
            self.button_index -=1

        print (self.button_index)

        self.button_index = self.button_index % len(self.button_list)
        self.current_button = self.button_list[self.button_index]

        if len(self.button_list) > 1:
            if increment:
                previous_button = self.button_list[(self.button_index -1 + len(self.button_list)) % len(self.button_list)]
            else:
                previous_button = self.button_list[(self.button_index + 1 + len(self.button_list)) % len(self.button_list)]

            previous_button.background_color = (0,0,0,0)

        self.current_button.background_color = (1,1,1,1)
        self.current_button.color = (0,0,0,1)

    
    def select(self):
        pass
    
    def deselect(self):
        pass