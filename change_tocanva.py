import customtkinter
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
import os 
import patoolib


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
                                           corner_radius = 20,
                                           border_width = 1
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

### -> Train Page Class
class Train_page(customtkinter.CTkFrame):
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
        - เป็นกดปุ่มขึ้นมาแล้วให้ Upload File (วางแผนไว้ว่าเป็นไฟล์ .zip, .rar)
        """
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
                                                    command = lambda : self.select_file())
        self.upload_button.pack(side = "top", expand = True)
        self.upload_button.bind("<Enter>", command = lambda event : self._on_enter())
        self.upload_button.bind("<Leave>", command = lambda event : self._on_leave())

        #### -> ฟังก์ชันสำหรับทำให้ตัวหนังสือเปลี่ยนสี
    def _on_enter(self):
        self.upload_button.configure(text_color = "white", fg_color = "#232F34")
    def _on_leave(self):
        self.upload_button.configure(text_color = "black", fg_color = "transparent")

        #### -> ฟังก์ชันสำหรับเลือก File
    def select_file(self):
        filetypes = [["All", "*.*"], ["zip files", "*.zip"], ["rar file", "*.rar"]]
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
        patoolib.extract_archive(zip_file_path, outdir = folder_name)

        tkinter.messagebox.showinfo(title = "Succesful", 
                                    message = "Upload Successfully")

### -> Train Page Class (กำลังทำ)
class Label_page(customtkinter.CTkFrame):
    def __init__(self, parent):
        
        # setup
        super().__init__(master = parent, 
                         fg_color = "white")

        """
        Zone สำหรับ menu จะเป็น Frame ใหญ่ประกอบด้วย
        1. Label Tools
        2. Class โชว์ class ทั้งหมด
        3. List ของ Image
        """
        self.count = 0
        # สร้างข้อมูลที่ใช้เก็บ bounding box
        self.bbox_data = []

        menu_side = customtkinter.CTkFrame(master = self,
                                           fg_color = "#D2DBE0",
                                           width = 280)
        menu_side.pack_propagate(False)
        menu_side.pack(side = "left",
                       fill = "both",
                       padx = 10,
                       pady = 10)
        

        """
            Annotation Frame (พวก rectangular, go back) sub_frame_1
        """
        sub_frame_1 = customtkinter.CTkFrame(master = menu_side,
                                             fg_color = "#232F34")
        sub_frame_1.pack(side = "top",
                         pady = 7,
                         padx = 7,
                         fill = "both")
        annotation_frame = customtkinter.CTkFrame(master = sub_frame_1,
                                                  fg_color = "transparent")
        annotation_frame.pack(side = "top",
                              padx = 10,
                              pady = 10,
                              fill = "x")
        hand_button = customtkinter.CTkButton(master = annotation_frame,
                                              fg_color = "white",
                                              bg_color = "transparent",
                                              image = customtkinter.CTkImage(Image.open(fp = "Icon_image/Hand.png"), 
                                                                             size = (30, 30)),
                                              text = "",
                                              width = 40,
                                              height = 36)
        hand_button.pack(side = "left", padx = 5)
        retangular_button = customtkinter.CTkButton(master = annotation_frame,
                                                    fg_color = "white",
                                                    bg_color = "transparent",
                                                    image = customtkinter.CTkImage(Image.open(fp = "Icon_image/rectangle_icon.png"),
                                                                                   size = (30, 30)),
                                                    text = "",
                                                    width =40,
                                                    height = 36)
        retangular_button.pack(side = "left", padx = 5)
        go_back_button = customtkinter.CTkButton(master = annotation_frame,
                                                 fg_color = "transparent",
                                                 bg_color = "transparent",
                                                 image = customtkinter.CTkImage(Image.open(fp = "Icon_image/go_back.png"),
                                                                                size = (30, 30)), 
                                                 text = "",
                                                 width = 40,
                                                 height = 36)
        go_back_button.pack(side = "left", padx = 5)
        go_back_button = customtkinter.CTkButton(master = annotation_frame,
                                                 fg_color = "transparent",
                                                 bg_color = "transparent",
                                                 image = customtkinter.CTkImage(Image.open(fp = "Icon_image/go_forward.png"),
                                                                                size = (30, 30)), 
                                                 text = "",
                                                 width = 40,
                                                 height = 36)
        go_back_button.pack(side = "left", padx = 5)


        """
            Class Tag sub_frame_1
        """
        class_frame = customtkinter.CTkFrame(master = sub_frame_1,
                                             fg_color = "black")
        class_frame.pack(side = "top",
                         padx = 7,
                         pady = 10)
        class_name_label = customtkinter.CTkLabel(master = class_frame,
                                                   font = ("Calibri Bold", 18),
                                                   text_color = "white",
                                                   text = "CLASSES")
        class_name_label.pack(side = "top")

        class_table = ttk.Treeview(master = class_frame,
                                   columns = ["No.", "Name"],
                                   show = "headings")
        class_table.pack(side = "top",
                         padx = 5,
                         pady = 5,
                         expand  = True)
        class_table.heading(column = "No.",
                            text = "No.")
        class_table.heading(column = "Name",
                            text = "Name")
        class_table.insert("", 0, values = (1, "None"))

        
        """
            Image List sub_frame_2
        """
        sub_frame_2 = customtkinter.CTkFrame(master = menu_side,
                                             fg_color = "#232F34")
        sub_frame_2.pack(side = "top",
                         pady = 7,
                         padx = 7,
                         fill = "both",
                         expand = True)
        border_frame = customtkinter.CTkFrame(master = sub_frame_2,
                                              fg_color = "black")
        border_frame.pack(expand = True, 
                          fill = "both",
                          padx = 7,
                          pady = 10)
        
        
        self.combo_box = ttk.Combobox(master = border_frame,
                                      state = "readonly",
                                      height = 10)
        self.get_folder()
        self.combo_box.set(value = "Select")
        self.combo_box.pack(side = "top")
        self.combo_box.bind("<<ComboboxSelected>>", 
                            func =  lambda event: self.update_treeview())


        tree_image_list_label = customtkinter.CTkLabel(master = border_frame,
                                                       text = "Image List",
                                                       font = ("Calibri Bold", 18),
                                                       text_color = "white")
        tree_image_list_label.pack(side = "top")
        self.tree_image_list = ttk.Treeview(master = border_frame,
                                       columns = ["No.", "Check"],
                                       show = "headings")
        self.tree_image_list.pack(expand = True,
                             fill = "both")
        self.tree_image_list.heading(column = "No.",
                                text = "No.")
        self.tree_image_list.heading(column = "Check",
                                text = "Check")
        self.tree_image_list.bind("<<TreeviewSelect>>",
                                  func = lambda event : self.select_image())
        # ตัวแปรสำหรับการลากเลือก
        self.rect = None
        self.img_tk = None

        
        """
            zone image
        """
        self.image_zone = tkinter.Canvas(master = self, bg = 'red')
        self.image_zone.pack(side= "left",
                             expand = True,
                             fill = "both")


        self.image_zone.bind("<Motion>", func = lambda event : print(f"x = {event.x} y = {event.y}"))
        self.image_zone.bind("<Button-1>", func = self.on_press)
        self.image_zone.bind("<B1-Motion>", func = self.on_drag)
        self.image_zone.bind("<ButtonRelease-1>", func = self.on_release)



    """
        ฟังก์ชันดึงชื่อของ Folder ไปใส่ใน Combobox
    """
    def get_folder(self):
        test = os.listdir()
        self.folder_list = []
        for i in test:
            if i[:6] == "Image_":
                self.folder_list.append(i)
            else:
                pass
        self.combo_box.configure(values = self.folder_list)
        

    """
        ฟังก์ชันดึงข้อมูลใน Folder ตามชื่อที่เลือกใน combobox
    """
    def update_treeview(self):
        # clear ทุก Item ใน treeview
        print("test")
        for item in self.tree_image_list.get_children():
            self.tree_image_list.delete(item)
        print(self.combo_box.get())
        # เพิ่ม Image ใน 
        for root, dirs, files in os.walk(self.combo_box.get()):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.tree_image_list.insert('', 'end', value = (file,))

        
    """
       ฟังก์ชันการเปลี่ยนรูปภาพตามรูปที่เราเลือก 
    """
    def select_image(self):

        selected_image = self.tree_image_list.selection()[0]
        print(selected_image)
        self.image_path_selected = self.combo_box.get() + "/" + self.tree_image_list.item(item = selected_image)["values"][0]
        print(f"path = {self.image_path_selected}")

        self.image_zone.delete("all")
        image = Image.open(self.image_path_selected)
        canvas_width = self.image_zone.winfo_width()
        canvas_height = self.image_zone.winfo_height()
        ratio = min(canvas_width / image.width, canvas_height / image.height)
        new_width = int(image.width * ratio)
        new_height = int(image.height * ratio)

        # ปรับขนาดของภาพ
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized_image)
        print(f"width = {resized_image.width}, height = {resized_image.height}")
        self.resized_image_width = resized_image.width
        self.resized_image_height = resized_image.height

        # ลบภาพเก่า (ถ้ามี)
        self.image_zone.delete("all")

        self.image_zone.create_image(0, 0, anchor=tkinter.NW, image=self.image)
        self.image_zone.image = self.image


    """
        ฟังก์ชันการลากแล้วกำหนดขอบเขตการ Label
    """
    def on_press(self, event):
        # เก็บตำแหน่งเริ่มต้นของการลากเลือก
        self.start_x = self.image_zone.canvasx(event.x)
        self.start_y = self.image_zone.canvasy(event.y)
        
        # สร้างกล่องสี่เหลี่ยมเริ่มต้น
        self.rect = self.image_zone.create_rectangle(self.start_x, 
                                                     self.start_y, 
                                                     self.start_x, 
                                                     self.start_y, 
                                                     outline="black", 
                                                     tags="current_rect"+f"{self.count}")
        
    def on_drag(self, event):
        # ปรับปรุงขนาดของกล่องสี่เหลี่ยมขณะลาก
        cur_x = self.image_zone.canvasx(event.x)
        cur_y = self.image_zone.canvasy(event.y)
        self.image_zone.coords("current_rect"+f"{self.count}", self.start_x, self.start_y, cur_x, cur_y)
    
    def on_release(self, event):
        # เก็บข้อมูล bounding box เมื่อปล่อยเมาส์
        end_x = self.image_zone.canvasx(event.x)
        end_y = self.image_zone.canvasy(event.y)
        bbox = (min(self.start_x, end_x), min(self.start_y, end_y), max(self.start_x, end_x), max(self.start_y, end_y))
        self.bbox_data.append(bbox)
        self.count += 1
        self.box_info()

    def box_info(self):
        print(self.bbox_data)
        # ล้างข้อมูล bounding box เก่า
        self.bbox_data = []
        
        
        



        

### -> Root App
class main(customtkinter.CTk):
    def __init__(self, title : str, height : int, width : int):
        super().__init__()

        """
        Set up our app
        """
        # self.attributes("-alpha", 0.96)
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
        # self.bind("<Motion>", func = lambda event : print(f"x = {event.x} y = {event.y}"))

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
main(title = "Personal outfit detection platform with YOLO", 
     height = 1500, 
     width = 750)