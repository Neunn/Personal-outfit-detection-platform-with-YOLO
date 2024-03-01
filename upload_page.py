import customtkinter
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
import os, shutil
import patoolib
# import yaml

class Upload_page(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = "white")

        # เป็นกรอบ Frame ภายใน โดย expand = True คือการขยาย widget ของเรา 
        inside_frame = customtkinter.CTkFrame(master = self,
                                              corner_radius = 20,
                                              fg_color = "#D2DBE0")
        inside_frame.pack(side = "top",
                          padx = 20,
                          pady = 30,
                          expand = True,
                          fill = "both")
        

        self.upload_button = customtkinter.CTkButton(master = inside_frame,
                                                    text = "Open Your File .zip",
                                                    compound = "top",
                                                    image = customtkinter.CTkImage(Image.open(fp = r"Icon_image/Upload_icon.png"),
                                                                                size = (100, 100)),
                                                    font = ("Calibri Bold", 40),
                                                    text_color = "black",
                                                    fg_color = "transparent",
                                                    corner_radius = 100,
                                                    width = 500,
                                                    height = 500,
                                                    command = lambda : self.select_file()) ### self.select_file คือ function ที่อยู่ภายใน Class นี้ ฟังก์ชันที่อยู่ใน Class เราจะเรียกว่า method โดย method self.select_file จะทำงานเมื่อเรากดปุ่ม 
        self.upload_button.pack(side = "top", expand = True)

        # สองบรรทัดข้างล่างนี้เป็นการ bind ปุ่มเวลาที่เรานำ pointer (เมาส์) ไปชี้หรือทำอะไรก็ตามกับปุ่มตามฟังก์ชันที่เราตั้งค่าไว้โดยในที่นี้เป็นการใช้ <Enter> และ <Leave> โดยที่ <Enter> คือมื่อนำ pointer เข้าไปในบริเวณวิดเจ็ตของปุ่ม ส่วน <Leave> คือการนำ pointer ออกมาบริเวณนอกวิดเจ็ตนั่นเอง
        self.upload_button.bind("<Enter>", command = lambda event : self.upload_button.configure(text_color = "white",
                                                                                             fg_color = "#232F34"))
        self.upload_button.bind("<Leave>", command = lambda event : self.upload_button.configure(text_color = "black",
                                                                                             fg_color = "transparent"))

        #### -> ฟังก์ชันสำหรับเลือก File
    def select_file(self):
        """
            ฟังก์ชันสำหรับเลือกไฟล์ที่เราจะทำการอัปโหลดในตอนนี้เป็น file ที่มีนามสกุลเป็น .zip, .rar และแตกไฟล์อัตโนมัติ
        """

        filetypes = [["zip files", "*.zip"], ["rar file", "*.rar"]]     # สร้าง list สำหรับประเภทของไฟล์ และคำที่จะใช้แสดง

        # สร้างหน้าต่างสำหรับการค้นหาไฟล์ โดยค่าที่ได้เราจะได้เป็น path ของไฟล์มาเก็บไว้ในตัวแปร zip_fil_path
        zip_file_path = fd.askopenfilename(title = "Open File Name",
                                            initialdir = "/",
                                            filetypes = filetypes)
        
        
        # ตรวจสอบว่าไฟล์ .zip มีอยู่จริงหรือไม่ หากมีก็ให้ผ่านไป แต่ หากไม่มีจะขึ้นโชว์หน้าต่าง Error ให้ขึ้นเลือกไฟล์ zip ใหม่แล้วจะเด้งออกจากฟังก์ชัน ด้วย return
        if not zip_file_path:
            tkinter.messagebox.showerror(title = "Error",
                                         message = "Please Select A Zip File!")
            return # <- เด้งออกจากฟังก์ชัน self.select_file
        

        # ต่อมาเราจะทำการแตกไฟล์ .zip, .rar ที่เราเลือกมา โดยขั้นแรกให้ทำการตรวจสอบใน workspace ของเราก่อนว่ามีโฟล์เดอร์ที่ขึ้นต้นด้วย Image_ ไหม หากมี ให้
        folder_name = "Image_1"
        counter = 2
        while os.path.exists(path = folder_name):
            folder_name = f"Image_{counter}"
            counter += 1
        os.makedirs(name = folder_name)

            # เปิด File Zip และ แตกไฟล์ใน Folder Image แต่ละครั้ง
        patoolib.extract_archive(zip_file_path, outdir = folder_name)

        tkinter.messagebox.showinfo(title = "Succesful", 
                                    message = "Upload Successfully")
