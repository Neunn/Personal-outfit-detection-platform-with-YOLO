import customtkinter
from PIL import Image
from home_page import Home_page
from train_page import Train_page
from label_page import Label_page
from upload_page import Upload_page
from report_page import Report_page




### -> Root App
class main(customtkinter.CTk):
    def __init__(self, title : str, height : int, width : int):
        super().__init__()

        """
        Set up our app
        """ 
        # pywinstyles.apply_style(window = self, style = "aero")
        self.geometry(geometry_string = f"{height}x{width}+0+0")
        self.title(string = title)
        self.configure(fg_color = "#f5f6fa")
        self.iconbitmap(bitmap = "Icon_image/nds-website-favicon-color.ico")

        """
        สร้าง Frame สำหรับบริเวณเมนูและเพิ่มปุ่มเข้าไป
        """
        self.menu_zone = customtkinter.CTkFrame(master = self,
                                                width = 110,
                                                fg_color = "#344955",
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
                                                        page_class = Report_page)
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
        # self.bind("<Motion>", func = lambda event : print(f"x = {event.x} y = {event.y}"))


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
        button.configure(text_color= "black", 
                         fg_color = "#fbc531", 
                         image = customtkinter.CTkImage(Image.open(fp = icon_path_hover), size = (70, 48)))
        
    def _on_leave(self, button, icon_path):
        button.configure(text_color = "white", 
                         fg_color = "transparent", 
                         image = customtkinter.CTkImage(Image.open(fp = icon_path), size = (70, 48)))

    #### -> ฟังก์ชันสำหรับเปลี่ยนหน้า
    def show_frame(self, page_class : object):
        for child in self.main_page.winfo_children():
            child.destroy()

        frame = page_class(parent = self.main_page)
        frame.pack(fill = "both",
                   expand = True)
        
        
### -> Run Application app
main_app = main(title = "Personal outfit detection platform with YOLO", 
    height = 1500, 
    width = 750)
main_app.mainloop()