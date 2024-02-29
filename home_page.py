import customtkinter
import tkinter
from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import filedialog as fd
# import os, shutil
# import patoolib
# import yaml

### -> Home Page Class
class Home_page(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = "white")
        
        """
        ส่วนประกอบหลักๆคือ
        ประกอบด้วย
        - top_frame : สำหรับคำ Welcome
        - second_frame : เนื้อหาการใช้งาน
        """

        # top_frame
        top_frame = customtkinter.CTkFrame(master = self,
                                           fg_color = "transparent")
        top_frame.pack(side = 'top')
        welcome_label = customtkinter.CTkLabel(master = top_frame,
                                       text = "Welcome",
                                       font = ("Calibri Bold", 60))
        welcome_label.pack(side = "top",
                           pady = 10, 
                          expand = True)
        
        # second_frame
        second_frame = customtkinter.CTkFrame(master = self,
                                              corner_radius = 20,
                                              fg_color = "#D2DBE0")
        second_frame.pack(side = "top",
                          expand = True,
                          fill = "both",
                          padx = 20,
                          pady = 20)
            # เพิ่ม text box ใน second_frame
        textbox = customtkinter.CTkTextbox(master = second_frame,
                                           font = ("Calibri Regular", 20),
                                           corner_radius = 20
                                           )
        textbox.pack(side = "top",
                     expand = True,
                     fill = "both",
                     padx = 20,
                     pady = 20)
        how_to = """        
                    ยินดีตอนรับเข้าสู่โปรแกรมของเราโปรแกรมนี้คือแพลทฟอร์ม All In One คุณสามารถสร้าง Model ของคุณภายในที่เดียว

                    โดยขั้นตอนการใช้งานมีดังนี้

                    1. เตรียมข้อมูลรูปภาพของคุณที่จะใช้ Train

                    2. อัปโหลดข้อมูลของคุณในเมนู Upload (เป็นไฟล์ .zip, .rar)

                    3. ทำการ Label รูปภาพของคุณ โดยคุณสามารถกำหนด Class ได้
                       (เมื่อกดปุ่มเทรนแล้วกรุณาอย่าปิดโปรแกรม)

                    4. ทำการ Train โมเดลของคุณโดยสามารถปรับพารามิเตอร์ได้

                    5. ดูผลของโมเดลได้ที่เมนู Report และสามารถทดลองใช้โมเดลที่เรา Train มาได้
                 """
        textbox.insert(index = "0.0",
                       text = how_to)
        textbox.configure(state = "disabled")