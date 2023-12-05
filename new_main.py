import customtkinter
import tkinter
from tkinter import ttk
from PIL import Image


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
        textbox = customtkinter.CTkTextbox(master = second_frame)
        textbox.pack(side = "top",
                     expand = True,
                     fill = "both",
                     padx = 20,
                     pady = 20)


### -> Label Page Class
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


### -> Root App
class main(customtkinter.CTk):
    def __init__(self, title : str, height : int, width : int):
        super().__init__()

        """
        Set up our app
        """
        self.geometry(geometry_string = f"{height}x{width}")
        self.title(string = title)
        self.configure(fg_color = "#f5f6fa")


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
                                                        page_class = Home_page)
        
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
                                                          page_class = Home_page)
        

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