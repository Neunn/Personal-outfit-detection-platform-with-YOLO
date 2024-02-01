import customtkinter
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
import os, shutil
import patoolib
import yaml

class Report_page(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = "white")

        """
        content inside
        """
        label = customtkinter.CTkLabel(master = self,
                                       text = "Report Page",
                                       font = ("Calibri Bold", 30))
        label.pack()