import customtkinter
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import os, shutil


class Report_page(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = "#D2DBE0")

        """
        content inside
        """
        ### แผนการทำงาน
        # 1. ต้องมีปุ่ม combobox สำหรับเลือก folder เพื่อโชว์ข้อมูลที่เทรนได้
        # 2. หากไม่มีโฟลเดอร์ที่เทรนให้ขึ้น show Error
        # 3. หากมีให้นำรูปหรือค่าต่างๆมาพล็อตเป็นกราฟต่างๆ สามารถเลื่อนดูได้
        
        ############## select zone ##############

        select_zone = customtkinter.CTkFrame(master = self,
                                             bg_color = "transparent",
                                             fg_color = "#39434b")
        select_zone.pack(padx = 5,
                         pady = 5,
                         fill = "both")
        

        select_label = customtkinter.CTkLabel(master = select_zone,
                                              text = "Parameter Report",
                                              font = ("Calibri Bold", 30),
                                              text_color = "#a1a9af")
        select_label.pack(pady = 15,
                          padx = 10,
                          side = "left")


        folder_combo_box = customtkinter.CTkComboBox(master = select_zone,
                                                     state = "readonly",
                                                     button_hover_color = "#a1a9af",
                                                     dropdown_hover_color= "#ffffff",
                                                     border_color = "#ffffff",
                                                     button_color = "#ffffff")
        folder_combo_box.pack(side = "right",
                              padx = 10,
                              pady = 15)
        folder_combo_box.set(value = "Select")


        ############## dashboard zone ##############
        dashboard_zone = customtkinter.CTkFrame(master = self,
                                                bg_color = "transparent",
                                                fg_color = "transparent")
        dashboard_zone.pack(fill = "both",
                            padx = 5,
                            pady = 5)
        
        ## setup column, row  : weight
        dashboard_zone.columnconfigure(index = 0, weight = 25)
        dashboard_zone.columnconfigure(index = 1, weight = 25)
        dashboard_zone.columnconfigure(index = 2, weight = 25)
        dashboard_zone.columnconfigure(index = 3, weight = 25)
        
        label_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                               bg = "white")
        label_canvas.grid(row = 0,
                          column = 0,
                          sticky = "WNE",
                          padx = 5,
                          pady = 5)
        
        p_curve_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                                 bg = "white")
        p_curve_canvas.grid(row = 0, 
                            column = 1,
                            sticky = "WNE",
                            padx = 5,
                            pady = 5)
        
        pr_curve_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                                 bg = "white")
        pr_curve_canvas.grid(row = 0, 
                            column = 2,
                            sticky = "WNE",
                            padx = 5,
                            pady = 5)
        
        r_curve_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                                 bg = "white")
        r_curve_canvas.grid(row = 0, 
                            column = 3,
                            sticky = "WNE",
                            padx = 5,
                            pady = 5)
        
        confusion_matrix_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                                          bg = "white")
        confusion_matrix_canvas.grid(row = 1,
                                     column = 0,
                                     columnspan = 2,
                                     sticky = "WNE",
                                     padx = 5,
                                     pady = 5)
        
        result_cavas = customtkinter.CTkCanvas(master = dashboard_zone,
                                               bg = "white")
        result_cavas.grid(row = 1, 
                          column = 2,
                          columnspan = 2,
                          sticky = "WNE",
                          padx = 5,
                          pady = 5)
        