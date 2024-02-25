import customtkinter
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
import os, shutil
import cv2
from app_demo import Main_demo

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


        self.folder_combo_box = customtkinter.CTkComboBox(master = select_zone,
                                                     state = "readonly",
                                                     button_hover_color = "#a1a9af",
                                                     dropdown_hover_color= "#ffffff",
                                                     border_color = "#ffffff",
                                                     button_color = "#ffffff",
                                                     command = lambda event : self.show_graph())
        self.folder_combo_box.pack(side = "right",
                              padx = 10,
                              pady = 15)
        self.folder_combo_box.set(value = "Select")
        self.get_folder()

        #### App demo
        app_button = customtkinter.CTkButton(master = select_zone,
                                             text =  "Try it out!",
                                             font = ("Calibri Bold", 15),
                                             command = lambda : Main_demo(parent = self,
                                                                          folder = self.folder_combo_box.get()))
        app_button.pack(side = "right")


        ############## dashboard zone ##############
        dashboard_zone = customtkinter.CTkScrollableFrame(master = self,
                                                bg_color = "transparent",
                                                fg_color = "transparent")
        dashboard_zone.pack(fill = "both",
                            expand = True,
                            padx = 5,
                            pady = 5)
        
        ## setup column, row  : weight
        dashboard_zone.columnconfigure(index = 0, weight = 25)
        dashboard_zone.columnconfigure(index = 1, weight = 25)
        dashboard_zone.columnconfigure(index = 2, weight = 25)
        dashboard_zone.columnconfigure(index = 3, weight = 25)
        
        self.label_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                               height = 400)
        self.label_canvas.grid(row = 0,
                          column = 0,
                          sticky = "WNE",
                          padx = 5,
                          pady = 5)
        
        self.p_curve_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                                 height = 400)
        self.p_curve_canvas.grid(row = 0, 
                            column = 1,
                            sticky = "WNE",
                            padx = 5,
                            pady = 5)
        
        self.pr_curve_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                                 height = 400)
        self.pr_curve_canvas.grid(row = 0, 
                            column = 2,
                            sticky = "WNE",
                            padx = 5,
                            pady = 5)
        
        self.r_curve_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                                 height = 400)
        self.r_curve_canvas.grid(row = 0, 
                            column = 3,
                            sticky = "WNE",
                            padx = 5,
                            pady = 5)
        
        self.confusion_matrix_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                                          height = 700)
        self.confusion_matrix_canvas.grid(row = 1,
                                     column = 0,
                                     columnspan = 2,
                                     sticky = "WNE",
                                     padx = 5,
                                     pady = 5)
        
        self.result_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                               height = 700)
        self.result_canvas.grid(row = 1, 
                          column = 2,
                          columnspan = 2,
                          sticky = "WNE",
                          padx = 5,
                          pady = 5)
        
        self.pred_canvas = customtkinter.CTkCanvas(master = dashboard_zone,
                                              height = 1000)
        self.pred_canvas.grid(row = 2,
                         column = 0,
                         columnspan = 4,
                         sticky = "WNES",
                         padx = 5,
                         pady = 5)
        

    def get_folder(self):
        folder_list = []
        for i in os.listdir():
            if i[:6] == "Image_":
                folder_list.append(i)

        self.folder_combo_box.configure(values = folder_list)
    
    def show_graph(self):
        self.label_canvas.delete("all")
        self.p_curve_canvas.delete("all")
        self.pr_curve_canvas.delete("all")
        self.r_curve_canvas.delete("all")
        self.confusion_matrix_canvas.delete("all")
        self.result_canvas.delete("all")
        self.pred_canvas.delete("all")

        self.label_canvas.configure(bg = "white")
        self.p_curve_canvas.configure(bg = "white")
        self.pr_curve_canvas.configure(bg = "white")
        self.r_curve_canvas.configure(bg = "white")
        self.confusion_matrix_canvas.configure(bg = "white")
        self.result_canvas.configure(bg = "white")
        self.pred_canvas.configure(bg = "white")



        label_image = Image.open(f"{self.folder_combo_box.get()}/runs/train/labels.jpg")
        self.label_canvas.bind("<Button-1>",
                               func = lambda event : self.full_screen_image(image_import=label_image,
                                                                            title_name = f"labels.png"))
        self.ratio_canvas(canvas_element = self.label_canvas,
                          image_import = label_image)
                          
        
        p_curve_image = Image.open(f"{self.folder_combo_box.get()}/runs/train/P_curve.png")
        self.p_curve_canvas.bind("<Button-1>",
                                 func = lambda event : self.full_screen_image(image_import = p_curve_image,
                                                                              title_name = f"P_curve.png"))
        self.ratio_canvas(canvas_element = self.p_curve_canvas,
                          image_import = p_curve_image)
        

        pr_curve_image = Image.open(f"{self.folder_combo_box.get()}/runs/train/PR_curve.png")
        self.pr_curve_canvas.bind("<Button-1>",
                                  func = lambda event : self.full_screen_image(image_import = pr_curve_image,
                                                                               title_name = f"PR_curve.png"))
        self.ratio_canvas(canvas_element = self.pr_curve_canvas,
                          image_import = pr_curve_image)
        

        r_curve_image = Image.open(f"{self.folder_combo_box.get()}/runs/train/R_curve.png")
        self.r_curve_canvas.bind("<Button-1>",
                                 func = lambda event : self.full_screen_image(image_import = r_curve_image,
                                                                              title_name = f"R_curve.png"))
        self.ratio_canvas(canvas_element = self.r_curve_canvas,
                          image_import = r_curve_image)
        

        confusion_matrix_image = Image.open(f"{self.folder_combo_box.get()}/runs/train/confusion_matrix.png")
        self.confusion_matrix_canvas.bind("<Button-1>",
                                          func = lambda event : self.full_screen_image(image_import = confusion_matrix_image,
                                                                                       title_name = f"confusion_matrix.png"))
        self.ratio_canvas(canvas_element = self.confusion_matrix_canvas,
                          image_import = confusion_matrix_image)
        

        result_image = Image.open(f"{self.folder_combo_box.get()}/runs/train/results.png")
        self.result_canvas.bind("<Button-1>",
                                func = lambda event : self.full_screen_image(image_import = result_image,
                                                                             title_name = "result.png"))
        self.ratio_canvas(canvas_element = self.result_canvas,
                          image_import = result_image)
        

        pred_image = Image.open(f"{self.folder_combo_box.get()}/runs/train/val_batch0_pred.jpg")
        self.pred_canvas.bind("<Button-1>",
                              func = lambda event : self.full_screen_image(image_import = pred_image,
                                                                           title_name = "predict image.png"))
        self.ratio_canvas(canvas_element = self.pred_canvas,
                          image_import = pred_image)


    # ฟังก์ชันแสดงรูปภาพใน canvas
    def ratio_canvas(self, canvas_element : object, image_import : object):
        canvas_height = canvas_element.winfo_height()
        canvas_width = canvas_element.winfo_width()
        ratio = min(canvas_height / image_import.height,
                    canvas_width / image_import.width)
        print(f"ratio = {ratio}")
        new_width = int(image_import.width * ratio)
        print(f"new_width = {new_width}")
        new_height = int(image_import.height * ratio)
        print(f"new_height = {new_height}")

        # ปรับขนาดของภาพ
        resized_image = image_import.resize((new_width, new_height),
                                            Image.BICUBIC)
        final_image = ImageTk.PhotoImage(image = resized_image)
        canvas_element.create_image(canvas_width/2,
                                    0,
                                    anchor = "n",
                                    image = final_image)
        canvas_element.image = final_image


    # ฟังก์ชันโชว์รูปภาพแบบเต็มจอ
    def full_screen_image(self, image_import : object, title_name : str):
        top_level = tkinter.Toplevel()
        top_level.geometry("500x500")
        top_level.title(f"{title_name}")
        top_level.after(ms = 250, 
                        func = lambda : top_level.iconbitmap("Icon_image/nds-website-favicon-color.ico"))

        self.im_copy = image_import.copy()
        image_import = image_import.resize((top_level.winfo_width(), 
                                            top_level.winfo_height()))
        image_tk = ImageTk.PhotoImage(image_import)
        
        self.background = tkinter.Label(master = top_level,
                                        image = image_tk)
        self.background.pack(expand = True,
                         fill = "both",
                         side = "top",
                         padx = 10,
                         pady = 10)

        self.background.image = image_tk
        top_level.bind("<Configure>", func = lambda event : self.responsive_resize(event = event))


    def responsive_resize(self, event):
        new_width = event.width
        new_height = event.height
        resize_image = self.im_copy.resize((new_width, new_height))
        final_image = ImageTk.PhotoImage(image = resize_image)
        self.background.configure(image = final_image)
        self.background.image = final_image


# ## Demo App
# class Main_demo(tkinter.Toplevel):
#     def __init__(self, title : str, geometry : list|tuple, folder : str, parent : object):
#         # สืบทอดทุก method ของ customtkinter.CTk ทั้งหมด
#         super().__init__(master = parent)

#         self.folder = folder
#         self.title(string = title)
#         self.geometry(f"{geometry[0]}x{geometry[1]}")
#         self.resizable(width = False, height = False)
#         self.columnconfigure(index = 0, weight = 5)
#         self.columnconfigure(index = 1, weight = 95)


#         menu_tab = Menu_tab(parent = self)
#         menu_tab.pack(side = "left",
#                       fill = "both")
#         cap  = cv2.VideoCapture(0)
#         self.video_area = tkinter.Canvas(master = self, 
#                                          bg = "red")
#         self.video_area.pack(side = "left",
#                              fill = "both",
#                              expand = True)
#         self.video_area.update()

#         print(f"Video Area = {self.video_area.winfo_height()}")
#         print(f"Video Area = {self.video_area.winfo_width()}")

#         self.count = 0 
#         print("test")
#         print()
#         self.show_video(cap = cap)
#         print(f"test end")



#     def show_video(self, cap):

#         # self.video_area.clear

#         self.video_area.delete("all")
#         ret, frame = cap.read()


#         if ret:
            
#             img_fromarray = Image.fromarray(cv2.cvtColor(src = frame,
#                                                          code = cv2.COLOR_BGR2RGB))
#             convert_image = self.resize_image_to_canvas_ratio(image_from_array = img_fromarray)
#             self.video_area.create_image(0,
#                                         0,
#                                         image = convert_image,
#                                         anchor = tkinter.NW)
#             self.video_area.update()
#             print("test")

#             # self.count += 1
#             # print(f"self.count = {self.count}")
#             # for i in self.video_area.children:
#             #     print(i)


#             # self.video_area.create_rectangle(boxes[0][0], boxes[0][1], boxes[0][2], boxes[0][3])
#             # self.video_area.convert_image = convert_image
#         self.after(ms = 15, func = lambda: self.show_video(cap = cap))
        


#     def resize_image_to_canvas_ratio(self, image_from_array):
#         canvas_height = self.video_area.winfo_height()
#         canvas_width = self.video_area.winfo_width()
#         ratio = min(canvas_height / image_from_array.height, canvas_width / image_from_array.width)

#         # ปรับขนาดของภาพ
#         resized_image = image_from_array.resize((canvas_width, canvas_height), Image.BICUBIC)
        
#         final_image = ImageTk.PhotoImage(resized_image)

#         del canvas_height, canvas_width, ratio
#         return final_image