# Import Library
import customtkinter
# import tkinter



class Menu_tab(customtkinter.CTkTabview):
    def __init__(self, parent):
        super().__init__(master = parent)

        ## Tabs
        self.add("Detection")
        self.add("Log")

        ## Widget   
        Detection_Frame(self.tab("Detection"))
        Log_Frame(self.tab("Log"))
        


class Detection_Frame(customtkinter.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = "red")
        self.pack(expand = True, fill = "both")


        
class Log_Frame(customtkinter.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = "blue")
        self.pack(expand = True, fill = "both")

        