import customtkinter
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
# from tkinter import filedialog as fd
import os, shutil
import patoolib
import yaml

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
        self.rectangle_bool = False # เอาไว้เช็คค่าสถานะปุ่ม
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
        self.hand_button = customtkinter.CTkButton(master = annotation_frame,
                                              fg_color = "white",
                                              bg_color = "transparent",
                                              image = customtkinter.CTkImage(Image.open(fp = "Icon_image/Hand.png"), 
                                                                             size = (30, 30)),
                                              text = "",
                                              width = 40,
                                              height = 36,
                                              command = lambda : self.hand_button_event())
        self.hand_button.pack(side = "left", padx = 5)
        self.rectangular_button = customtkinter.CTkButton(master = annotation_frame,
                                                    fg_color = "white",
                                                    bg_color = "transparent",
                                                    image = customtkinter.CTkImage(Image.open(fp = "Icon_image/rectangle_icon.png"),
                                                                                   size = (30, 30)),
                                                    text = "",
                                                    width =40,
                                                    height = 36,
                                                    command = lambda : self.rectangle_button_event())
        self.rectangular_button.pack(side = "left", padx = 5)

        go_back_button = customtkinter.CTkButton(master = annotation_frame,
                                                 fg_color = "transparent",
                                                 bg_color = "transparent",
                                                 image = customtkinter.CTkImage(Image.open(fp = "Icon_image/go_back.png"),
                                                                                size = (30, 30)), 
                                                 text = "",
                                                 width = 40,
                                                 height = 36,
                                                 command = lambda : self.redo_event())
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

        self.class_table = ttk.Treeview(master = class_frame,
                                   columns = ["No.", "Name"],
                                   show = "headings")
        self.class_table.pack(side = "top",
                         padx = 5,
                         pady = 5,
                         expand  = True)
        self.class_table.heading(column = "No.",
                            text = "No.")
        self.class_table.heading(column = "Name",
                            text = "Name")
        
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
        self.scrollbar = ttk.Scrollbar(master = border_frame,
                                       orient = "vertical",
                                       command = self.tree_image_list.yview)
        self.tree_image_list["yscrollcommand"] = self.scrollbar.set
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
                             fill = "both",
                             padx = 20,
                             pady = 20)


        # self.image_zone.bind("<Motion>", func = lambda event : print(f"x = {event.x} y = {event.y}"))
        self.image_zone.bind("<Button-1>", func = self.on_press)
        self.image_zone.bind("<B1-Motion>", func = self.on_drag)
        self.image_zone.bind("<ButtonRelease-1>", func = self.on_release)

    def redo_event(self):    
        message_bool = tkinter.messagebox.askyesno(title = "แจ้งเตือน",
                                    message = "คุณต้องการที่จะ label รูปภาพนี้ใหม่ใช่หรือไม่?")
        if message_bool == True:
            if os.path.exists(path = os.path.splitext(self.image_path_selected)[0] + ".txt"):
                os.remove(path = os.path.splitext(self.image_path_selected)[0] + ".txt")
                tkinter.messagebox.showinfo(title = "Infomation",
                                            message = "ย้อนกลับใหม่เรียบร้อยแล้ว")
                self.image_zone.delete("all")

                ## update ค่า True เป็น "" หลังจากลบ
                focused = self.tree_image_list.focus()
                self.tree_image_list.item(focused, 
                                          text = "", 
                                          values = (self.tree_image_list.item(focused)["values"][0], ""))

                
            else:
                tkinter.messagebox.showerror(title = "Error",
                                             message = "ยังไม่มีการสร้างไฟล์ label")
        else:
            pass

    def hand_button_event(self):
        """ฟังก์ชันเช็ค ว่าเลือกเครื่องมือถูกไหม"""
        self.rectangle_bool = False
        self.hand_button.configure(fg_color = "#65B741")
        self.rectangular_button.configure(fg_color = "white")
        
    def rectangle_button_event(self):
        """ฟังก์ชันเช็ค ว่าเลือกเครื่องมือถูกไหม"""
        self.rectangle_bool = True
        self.hand_button.configure(fg_color = "white")
        self.rectangular_button.configure(fg_color = "#65B741")

    def update_classtree(self):
        """ฟังก์ชันดึงข้อมูลจาก file data.yaml"""
        if os.path.exists(path = f"{self.combo_box.get()}/data.yaml"):

            for item in self.class_table.get_children():
                self.class_table.delete(item)

            with open(file = f"{self.combo_box.get()}/data.yaml", mode = "r") as file:
                data = yaml.safe_load(file)

            for i,j in enumerate(data["names"]):
                self.class_table.insert("", 0, values = (i, j))

        else:
            for item in self.class_table.get_children():
                self.class_table.delete(item)

    
    def get_folder(self):
        """ฟังก์ชันดึงชื่อของ Folder ไปใส่ใน Combobox"""
        test = os.listdir()
        self.folder_list = []
        for i in test:
            if i[:6] == "Image_":
                self.folder_list.append(i)
            else:
                pass
        self.combo_box.configure(values = self.folder_list)
        
    
    def update_treeview(self):
        """ฟังก์ชันดึงข้อมูลใน Folder ตามชื่อที่เลือกใน combobox"""
        # อัปเดตตารางคลาส
        self.update_classtree()

        # clear ทุก Item ใน treeview
        for item in self.tree_image_list.get_children():
            self.tree_image_list.delete(item)
        print(self.combo_box.get())
        print("")
        # เพิ่ม Image ใน 
        for i in os.listdir(f"{self.combo_box.get()}"):
            if i.lower().endswith(('.png', '.jpg', '.jpeg')):
                if os.path.exists(path = f"{self.combo_box.get()}/{os.path.splitext(i)[0]}.txt"):
                    self.tree_image_list.insert('', 'end', value = (i,"True"))
                else:
                    self.tree_image_list.insert("", "end", values = (i, ""))
        


    def select_image(self):
        """
        ฟังก์ชันการเปลี่ยนรูปภาพตามรูปที่เราเลือก 
        """
        try:
            self.count = 0
            self.tree_image_list.focus_set()
            selected_image = self.tree_image_list.focus()
            
            print("")
            print(f"selected_image = {selected_image}")
            print("")
            # print(f"self.tree_image_list.item(item = selected_image)['values'][0] = {self.tree_image_list.item(item = selected_image)['values'].values()}")
            print("")
            self.image_path_selected = self.combo_box.get() + "/" + self.tree_image_list.item(item = selected_image)["values"][0]
            print(f"path = {self.image_path_selected}")
            print("")

            self.image_zone.delete("all")
            image = Image.open(self.image_path_selected)
            canvas_width = self.image_zone.winfo_width()
            canvas_height = self.image_zone.winfo_height()
            ratio = min(canvas_width / image.width, canvas_height / image.height)
            new_width = int(image.width * ratio)
            new_height = int(image.height * ratio)

            # ปรับขนาดของภาพ
            resized_image = image.resize((new_width, new_height), Image.BICUBIC)
            self.image = ImageTk.PhotoImage(resized_image)
            print(f"width = {resized_image.width}, height = {resized_image.height}")
            self.resized_image_width = resized_image.width
            self.resized_image_height = resized_image.height

            # ลบภาพเก่า (ถ้ามี)
            self.image_zone.delete("all")

            self.image_zone.create_image(0, 0, anchor=tkinter.NW, image=self.image)
            self.image_zone.image = self.image
            self.show_old_label()
        except:
            pass


    def on_press(self, event):
        """
        ฟังก์ชันการลากแล้วกำหนดขอบเขตการ Label
        """
        if self.rectangle_bool == True:
            # เก็บตำแหน่งเริ่มต้นของการลากเลือก
            self.start_x = self.image_zone.canvasx(event.x)
            self.start_y = self.image_zone.canvasy(event.y)
            
            # สร้างกล่องสี่เหลี่ยมเริ่มต้น
            self.rect = self.image_zone.create_rectangle(self.start_x, 
                                                        self.start_y, 
                                                        self.start_x, 
                                                        self.start_y, 
                                                        outline="red", 
                                                        tags= "current_rect"+f"{self.count}",
                                                        width = 3)
        else:
            print("เลือกเครื่องมือก่อน")

    def on_drag(self, event):
        if self.rectangle_bool == True:
            # ปรับปรุงขนาดของกล่องสี่เหลี่ยมขณะลาก
            cur_x = self.image_zone.canvasx(event.x)
            cur_y = self.image_zone.canvasy(event.y)
            self.image_zone.coords("current_rect"+f"{self.count}", self.start_x, self.start_y, cur_x, cur_y)
        else:
            pass
    
    def on_release(self, event):
        if self.rectangle_bool == True:
            # เก็บข้อมูล bounding box เมื่อปล่อยเมาส์
            end_x = self.image_zone.canvasx(event.x)
            end_y = self.image_zone.canvasy(event.y)
            bbox = (min(self.start_x, end_x), min(self.start_y, end_y), max(self.start_x, end_x), max(self.start_y, end_y))
            self.bbox_data.append(bbox)
            self.count += 1
            self.box_info()
        else:
            pass

    def box_info(self):
        """
            Yolo Format
                xmin: top-left x coordinate,
                ymin: top-left y coordinate,
                w: bounding box width,
                h: bounding box height,
                w_img: image width,
                h_img: image height
        """
        print("")
        print("bbox_data = ",self.bbox_data[0])
        w = abs(self.bbox_data[0][0] - self.bbox_data[0][2])
        h =abs(self.bbox_data[0][1] - self.bbox_data[0][3])
        self.x_center = float(int(self.bbox_data[0][0] + (w/2))/self.resized_image_width)
        self.y_center = float(int(self.bbox_data[0][1] + (h/2))/self.resized_image_height)
        self.w = float(w/self.resized_image_width)
        self.h = float(h/self.resized_image_height)
        print("")
        print(f"x_center = {self.x_center} y_center = {self.y_center}")
        print(f"w = {self.w} h = {self.h}")
        print("")
        self.tag_select()
        # ล้างข้อมูล bounding box เก่า
        self.bbox_data = []


    def tag_select(self):
        """หน้าต่าง top level เวลาลาก box เสร็จ"""

        # setup
        self.top = customtkinter.CTkToplevel(master = self)
        self.top.after(250, lambda : self.top.iconbitmap("Icon_image/nds-website-favicon-color.ico"))
        top_width = 300
        top_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width/2) - (top_width/2)
        y = (screen_height/2) - (top_height/2)
        self.top.title(string = "Tag Select")
        self.top.geometry(geometry_string = f"{top_width}x{top_height}+{int(x)}+{int(y)}")
        self.top.config(bg = "white")
        self.top.resizable(False, False)
        self.top.grab_set()
        
        # Widget
        label = customtkinter.CTkLabel(master = self.top,
                                       font = ("Calibri Bold", 18),
                                       text = "Select/Create Tags")
        label.pack(fill = "x")
        
        self.select_tag_combo_box = ttk.Combobox(master = self.top,
                                                 state = "readonly",
                                                 height = 20)
        
        self.select_tag_combo_box.set(value = "Select")
        self.select_tag_combo_box.pack(pady = 10)


        self.entry_widget_var = tkinter.StringVar()
        self.entry_widget = customtkinter.CTkEntry(master = self.top,
                                                   width = 140,
                                                   bg_color = "white",
                                                   fg_color = "white",
                                                   textvariable = self.entry_widget_var)
        self.entry_widget.pack(pady = 5)

        enter_button = tkinter.ttk.Button(master = self.top,
                                               text = "Enter",
                                               command = lambda : self.insert_tag())
        enter_button.pack(side = "top",
                          padx = 5)

        self.check_yaml_file()

        self.select_tag_combo_box.bind("<<ComboboxSelected>>", func = lambda event : self.entry_widget_var.set(""))
        self.entry_widget.bind("<Key>", command = lambda event : self.select_tag_combo_box.set(value = "Select"))

        self.top.bind("<Return>", func = lambda event : self.insert_tag())
    
    def check_yaml_file(self):
        if os.path.exists(path = f"{self.combo_box.get()}/data.yaml"):
            print("")
            print(f"พบเจอ file data.yaml path : {self.combo_box.get()}/data.yaml")
            print("")
            with open(file = f"{self.combo_box.get()}/data.yaml", mode = "r") as read_file:
                data = yaml.safe_load(read_file)
                self.select_tag_combo_box.configure(values = data["names"])
            pass
        else:
            with open(file = f"{self.combo_box.get()}/data.yaml", mode = "w") as file:
                yaml.dump({"names" : [], "nc" : 0},file)
                file.close()
    


    def insert_tag(self):

        # 0. entry ครั้งแรกตั้งเงื่อนไข
        # 1. เลือกคือการเลือกของที่มีอยู่แล้วสร้างไฟล์ใหม่
        # 2. entry คือการสร้าง label ใหม่แล้วสร้างไฟล์แท็ก Label
        # 3. หากเลือกต้องเคลียค่า entry

        path = f"{self.combo_box.get()}/data.yaml"
        im_select_path = os.path.splitext(self.image_path_selected)[0]
        print("new path = ", im_select_path)

        with open(file = path, mode = "r") as read_file:
            data = yaml.safe_load(read_file)
        print("data =", data)

        if self.select_tag_combo_box.get() == "Select" and self.entry_widget_var.get().strip().lower() == "":
            tkinter.messagebox.showerror(title = "Error",
                                         message = "กรุณาเลือก/เพิ่ม Tag")
            return

        if self.select_tag_combo_box.get() != "Select":
            print(f"Select Tag = {self.select_tag_combo_box.get()}")
            if os.path.exists(path = f"{im_select_path}.txt"):
                print("มีไฟล์ txt อยู่แล้ว")
                with open(file = f"{im_select_path}.txt", mode = "a") as read_file:

                    with open(file = path, mode = "r") as yaml_read_file:
                        data_read = yaml.safe_load(yaml_read_file)
                        
                        for i,j in enumerate(data_read["names"]):
                            if j == self.select_tag_combo_box.get():
                                index = i
                                break

                    line = f"\n{index} {self.x_center} {self.y_center} {self.w} {self.h}".rstrip()
                    read_file.write(line)
                self.update_classtree()
                self.tree_image_list.set(self.tree_image_list.focus(), "#2", "True")
                self.top.destroy()

            else:
                print("ไม่มีไฟล์สร้างใหม่")
                with open(file = f"{im_select_path}.txt", mode = "w") as write_file:

                    with open(file = path, mode = "r") as yaml_read_file:
                        data_read = yaml.safe_load(yaml_read_file)

                        for i,j in enumerate(data_read["names"]):
                            if j == self.select_tag_combo_box.get():
                                index = i
                                break

                    line = f"{index} {self.x_center} {self.y_center} {self.w} {self.h}".strip()
                    write_file.write(line)
                self.update_classtree()
                self.tree_image_list.set(self.tree_image_list.focus(), "#2", "True")
                self.top.destroy()


        elif self.entry_widget_var.get().strip().lower() != "":

            for i in data["names"]:
                if i == self.entry_widget_var.get().strip().lower():
                    print("มีชื่อ class นี้อยู่แล้วเดิมอยู่แล้ว")
                    
                    with open(file = f"{im_select_path}.txt", mode = "a") as read_file:
                        with open(file = path, mode = "r") as yaml_read_file:
                            data_read = yaml.safe_load(yaml_read_file)
                            
                            for j,k in enumerate(data_read["names"]):
                                if k == self.entry_widget_var.get().strip().lower():
                                    index = j
                                    break
                        

                        if os.stat(f"{im_select_path}.txt").st_size == 0:
                            line = f"{index} {self.x_center} {self.y_center} {self.w} {self.h}".rstrip()
                        else:
                            line = f"\n{index} {self.x_center} {self.y_center} {self.w} {self.h}".rstrip()

                        read_file.write(line)
                    self.tree_image_list.set(self.tree_image_list.focus(), "#2", "True")
                    self.top.destroy()
                    return
                else:
                    pass


            data["names"].append(self.entry_widget_var.get().strip().lower())
            data["nc"] += 1

            if os.path.exists(path = f"{im_select_path}.txt"):
                with open(file = path, mode = "w") as write_file:
                    yaml.dump(data, write_file)
                with open(file = path, mode = "r") as read_file:
                    data_read = yaml.safe_load(read_file)
                    for i,j in enumerate(data_read["names"]):
                        if j == self.entry_widget_var.get().strip().lower():
                            index = i
                            break

                with open(file = f"{im_select_path}.txt", mode = "a") as write_file:
                    line = f"\n{index} {self.x_center} {self.y_center} {self.w} {self.h}".rstrip()
                    write_file.write(line)
                    
            else:
                with open(file = path, mode = "w") as write_file:
                    yaml.dump(data, write_file)
                with open(file = path, mode = "r") as read_file:
                    data_read = yaml.safe_load(read_file)
                    for i,j in enumerate(data_read["names"]):
                        if j == self.entry_widget_var.get().strip().lower():
                            index = i
                            break


                    with open(f"{im_select_path}.txt", mode = "w") as txt_file:
                        line = f"{index} {self.x_center} {self.y_center} {self.w} {self.h}".rstrip()
                        txt_file.write(line)
            self.update_classtree()
            self.tree_image_list.set(self.tree_image_list.focus(), "#2", "True")
            self.top.destroy()
        

    def show_old_label(self):
        im_select_path = os.path.splitext(self.image_path_selected)[0]
        if os.path.exists(path = im_select_path + ".txt"):
            with open(file = im_select_path + ".txt", mode = "r") as read_file:
                data = read_file.readlines()
                info = []
                for i in data:
                    sub_info = [sub for sub in i.split(sep = " ")]
                    print("sub_info =",sub_info)
                    for j, k in enumerate(sub_info):
                        if j == 0:
                            sub_info[j] = int(k)
                        else:
                            sub_info[j] = float(k)
                    # print(f"new sub info = {sub_info}")
                    info.append(sub_info)
                    sub_info = []

                # print(f"info = {info}")

                ## Draw box
                for i in info:
                    x_center, y_center, w, h = i[1:]
                    x_start = (x_center - w/2) * self.resized_image_width
                    y_start = (y_center - h/2) * self.resized_image_height
                    x_end = (x_center + w/2) * self.resized_image_width
                    y_end = (y_center + h/2) * self.resized_image_height
                    self.image_zone.create_rectangle(x_start,
                                                     y_start,
                                                     x_end,
                                                     y_end,
                                                     width = 3,
                                                     outline = "green")



            print("show old label")
        else:
            print("No old label")
            pass
