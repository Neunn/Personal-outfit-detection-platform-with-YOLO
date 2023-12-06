import customtkinter
import tkinter
from tkinter import ttk
from PIL import Image
from tkinter import filedialog as fd
import os 
import zipfile

### -> Home Page Class
class Home_page(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = "white")
        
        """
        Content Inside
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
                                              corner_radius = 20)
        second_frame.pack(side = "top",
                          expand = True,
                          fill = "both",
                          padx = 20,
                          pady = 20)
            # เพิ่ม text box ใน second_frame
        textbox = customtkinter.CTkTextbox(master = second_frame,
                                           font = ("Calibri Regular", 20),
                                           corner_radius = 20,
                                           border_width = 2
                                           )
        textbox.pack(side = "top",
                     expand = True,
                     fill = "both",
                     padx = 20,
                     pady = 20)
        how_to = """        
                    ยินดีตอนรับเข้าสู่โปรแกรมของเราโปรแกรมนี้คือแพลทฟอร์ม All In One คุณสามารถสร้าง Model ภายในที่เดียว

                    โดยขั้นตอนการใช้งานมีดังนี้

                    1. เตรียมข้อมูลรูปภาพของคุณที่จะใช้ Train

                    2. อัปโหลดข้อมูลของคุณในเมนู Upload (เป็นไฟล์ .zip)

                    3. ทำการ Label รูปภาพของคุณ โดยคุณสามารถกำหนด Class ได้

                    4. ทำการ Train โมเดลของคุณโดยสามารถปรับพารามิเตอร์ได้

                    5. ดูผลของโมเดลได้ที่เมนู Report
                 """
        textbox.insert(index = "0.0",
                       text = how_to)
        textbox.configure(state = "disabled")

### -> Label Page Class (ยังก่อนยังไม่ทำ)
class Label_page(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color= "white")
        
        """
        Content Inside
        """
        label = customtkinter.CTkLabel(master = self,
                                       text = "Page 2",
                                       font = ("Calibri Bold", 30))
        label.pack(side = "top")

### -> Upload Page Class
class Upload_page(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = "white")

        """
        Content Inside
        - เป็นกดปุ่มขึ้นมาแล้วให้ Upload File (วางแผนไว้ว่าเป็นไฟล์ .zip)
        """
        inside_frame = customtkinter.CTkFrame(master = self,
                                              corner_radius = 20)
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
                                                    command = lambda : self.select_file())
        self.upload_button.pack(side = "top", expand = True)
        self.upload_button.bind("<Enter>", command = lambda event : self._on_enter())
        self.upload_button.bind("<Leave>", command = lambda event : self._on_leave())

        #### -> ฟังก์ชันสำหรับทำให้ตัวหนังสือเปลี่ยนสี
    def _on_enter(self):
        self.upload_button.configure(text_color = "white", fg_color = "#36719F")
    def _on_leave(self):
        self.upload_button.configure(text_color = "black", fg_color = "transparent")

        #### -> ฟังก์ชันสำหรับเลือก File
    def select_file(self):
        filetypes = [["zip files", "*.zip"]]
        zip_file_path = fd.askopenfilename(title = "Open File Name",
                                            initialdir = "/",
                                            filetypes = filetypes)
        
        
            # ตรวจสอบว่าไฟล์ .zip มีอยู่จริงหรือไม่
        if not zip_file_path:
            tkinter.messagebox.showerror(title = "Error",
                                         message = "Please Select A Zip File!")
            return
        
            # Check ว่าใน workspace ของเรามี Folder ที่ชื่อ Image อยู่รึไม่
        folder_name = "Image_1"
        counter = 2
        while os.path.exists(path = folder_name):
            folder_name = f"Image_{counter}"
            counter += 1
        os.makedirs(name = folder_name)

            # เปิด File Zip และ แตกไฟล์ใน Folder Image แต่ละครั้ง
        with zipfile.ZipFile(file = zip_file_path, mode = "r") as file:
            file.extractall(path = folder_name)

        tkinter.messagebox.showinfo(title = "Succesful", 
                                    message = "Upload Successfully")

### -> Train Page Class
class Train_page(customtkinter.CTkFrame):
    def __init__(self, parent):
        
        # setup
        super().__init__(master = parent, fg_color = "white")

        """
        Zone สำหรับ menu จะเป็น Frame ใหญ่ประกอบด้วย
        1. Label Tools
        2. Class โชว์ class ทั้งหมด
        3. List ของ Image
        """

        menu_side = customtkinter.CTkFrame(master = self,
                                           fg_color = "blue",
                                           width = 265)
        menu_side.pack(side = "left",
                       fill = "both")
        
        annotation_frame = customtkinter.CTkFrame(master = menu_side,
                                                  fg_color = "black")
        annotation_frame.pack(side = "top")



### -> Root App
class main(customtkinter.CTk):
    def __init__(self, title : str, height : int, width : int):
        super().__init__()

        """
        Set up our app
        """
        self.attributes("-alpha", 0.96)
        # pywinstyles.apply_style(window = self, style = "aero")
        self.geometry(geometry_string = f"{height}x{width}")
        self.title(string = title)
        self.configure(fg_color = "#f5f6fa")
        self.iconbitmap(bitmap = "Icon_image/nds-website-favicon-color.ico")

        """
        สร้าง Frame สำหรับบริเวณเมนูและเพิ่มปุ่มเข้าไป
        """
        self.menu_zone = customtkinter.CTkFrame(master = self,
                                                width = 110,
                                                fg_color = "#273c75",
                                                bg_color = "transparent",
                                                corner_radius = 0)
        self.menu_zone.pack_propagate(False)
        self.menu_zone.pack(side = "left", fill = "y")
        self.top_menu_zone_frame = customtkinter.CTkFrame(master = self.menu_zone,                                              
                                                          fg_color = "transparent")
        self.top_menu_zone_frame.pack(side = "top", fill = "y")
        self.bottom_menu_zone_frame = customtkinter.CTkFrame(master = self.menu_zone,
                                                             fg_color = "transparent")
        self.bottom_menu_zone_frame.pack(side = "bottom", fill = "y")

        """สร้างปุ่ม"""
        self.home_button_menu = self.create_menu_button(name = "Home",
                                                        menu_zone_frame = self.top_menu_zone_frame,
                                                        icon_path = "Icon_image/Home Page_white.png",
                                                        icon_path_hover = "Icon_image/Home Page.png",
                                                        page_class = Home_page)
        
        self.label_button_menu = self.create_menu_button(name = "Label",
                                                        menu_zone_frame = self.top_menu_zone_frame,
                                                        icon_path = "Icon_image/Label_white.png",
                                                        icon_path_hover = "Icon_image/Label.png",
                                                        page_class = Label_page)
        
        self.train_button_menu = self.create_menu_button(name = "Train",
                                                        menu_zone_frame = self.top_menu_zone_frame,
                                                        icon_path = "Icon_image/Train_white.png",
                                                        icon_path_hover = "Icon_image/Train.png",
                                                        page_class = Train_page)
        
        self.report_button_menu = self.create_menu_button(name = "Report",
                                                        menu_zone_frame = self.top_menu_zone_frame,
                                                        icon_path = "Icon_image/paper_white.png",
                                                        icon_path_hover = "Icon_image/paper.png",
                                                        page_class = Label_page)
            #ปุ่ม upload
        self.upload_button_menu = self.create_menu_button(name = "Upload",
                                                          menu_zone_frame = self.bottom_menu_zone_frame,
                                                          icon_path = "Icon_image/Upload_white.png",
                                                          icon_path_hover = "Icon_image/Upload.png",
                                                          page_class = Upload_page)
        

        """
        สร้างพื้นที่แสดงแต่ละ Page
        """
        self.main_page = customtkinter.CTkFrame(master = self, 
                                                fg_color = "transparent")
        self.main_page.pack(side="left", fill="both", expand=True)
        
        self.show_frame(page_class = Home_page)

        """
        ให้มันรันวน loop ไปเรื่อยๆ
        """
        self.mainloop()
    

    #### ฟังก์ชันสำหรับสร้างปุ่มแล้ว pack เข้าไปใน menu_zone
    def create_menu_button(self, name : str, menu_zone_frame : object, icon_path : str, icon_path_hover : str,
                           page_class : object):
        button = customtkinter.CTkButton(master = menu_zone_frame,
                                            image = customtkinter.CTkImage(Image.open(fp = icon_path), size = (70, 48)),
                                            compound = "top",
                                            text = name,
                                            text_color = "white",
                                            font = ("Calibri Bold", 24),
                                            fg_color = "transparent",
                                            command = lambda : self.show_frame(page_class = page_class),
                                            hover = False)
        button.bind("<Enter>", command = lambda event : self._on_enter(button = button, icon_path_hover = icon_path_hover))
        button.bind("<Leave>", command = lambda event : self._on_leave(button = button, icon_path = icon_path))

        button.pack(fill = "x", pady = 15, padx = 5)
        return button

    #### -> ฟังก์ชันสำหรับทำให้ปุ่มเปลี่ยนสี
    def _on_enter(self, button, icon_path_hover):
        button.configure(text_color= "black", fg_color = "#fbc531", 
                         image = customtkinter.CTkImage(Image.open(fp = icon_path_hover), size = (70, 48)))
    def _on_leave(self, button, icon_path):
        button.configure(text_color= "white", fg_color = "transparent", 
                         image = customtkinter.CTkImage(Image.open(fp = icon_path), size = (70, 48)))

    #### -> ฟังก์ชันสำหรับเปลี่ยนหน้า
    def show_frame(self, page_class : object):
        for child in self.main_page.winfo_children():
            child.destroy()

        frame = page_class(parent=self.main_page)
        frame.pack(fill="both", expand=True)

### -> Run Application app
main(title = "Personal outfit detection platform with YOLO", 
     height = 1500, 
     width = 750)