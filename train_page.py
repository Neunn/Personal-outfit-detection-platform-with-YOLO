import customtkinter
import tkinter
from tkinter import ttk
# from PIL import Image, ImageTk
# from tkinter import filedialog as fd
import os, shutil
import yaml
import numpy as np
from ultralytics import YOLO

### -> Train Page Class (กำลังทำ)
class Train_page(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color= "white")
        
        """
        หน้านี้เป็นเนื้อหาหลัก
        """

        inside_frame = customtkinter.CTkFrame(master = self,
                                               corner_radius = 20,
                                               fg_color = "#D2DBE0")
        inside_frame.pack(side = "top",
                          padx = 20,
                          pady = 10,
                          expand = True,
                          fill = "both")
        
        ### setup column weight
        inside_frame.columnconfigure(index = 0, weight = 2)
        inside_frame.columnconfigure(index = 1, weight = 2)
        inside_frame.columnconfigure(index = 3, weight = 16)


        ### All element
        title_label = customtkinter.CTkLabel(master = inside_frame,
                                             text = "Configuration",
                                             font = ("Calibri Bold", 25))
        title_label.grid(row = 0, 
                         column = 0,
                         sticky = "N",
                         pady = 10)


        choose_model_label = customtkinter.CTkLabel(master = inside_frame, 
                                                    text = "Choose pretrained model",
                                                    font = ("Calibri Light", 16))
        choose_model_label.grid(row = 1, 
                                column = 0,
                                sticky = "W",
                                padx = 10,
                                pady = 0)

        self.model_combo_box = customtkinter.CTkComboBox(master = inside_frame,
                                                    state = "readonly",
                                                    values = ["yolov8n.pt", 
                                                              "yolov8s.pt",
                                                              "yolov8m.pt",
                                                              "yolov8l.pt",
                                                              "yolov8x.pt"],
                                                    hover = True)
        self.model_combo_box.set("Select")
        self.model_combo_box.grid(row = 2, 
                             column = 0,
                             sticky = "WE",
                             padx = 10,
                             pady = 10)
        

        folder_select_label = customtkinter.CTkLabel(master = inside_frame,
                                                     text = "Folder Select",
                                                     font = ("Calibri Light", 16))
        folder_select_label.grid(row = 1,
                                 column = 1,
                                 sticky = "W",
                                 padx = 10)
        
        self.folder_combo_box = customtkinter.CTkComboBox(master = inside_frame,
                                                          state = "readonly")
        self.folder_combo_box.set("Select")
        self.folder_combo_box.grid(row = 2,
                              column = 1,
                              columnspan = 2, 
                              padx = 5,
                              sticky = "WE")
        
        folder_list = self.get_folder()
        self.folder_combo_box.configure(values = folder_list)




        train_test_label = customtkinter.CTkLabel(master = inside_frame, 
                                                    text = "Train / Test %",
                                                    font = ("Calibri Light", 16))
        train_test_label.grid(row = 3, 
                              column = 0, 
                              sticky = "W",
                              padx = 10,
                              pady = 5)

        self.slider_train_test_variable = tkinter.IntVar()
        self.slider_train_test = customtkinter.CTkSlider(master = inside_frame,
                                                from_ = 0,
                                                to = 100,
                                                number_of_steps = 100,
                                                hover = True,
                                                variable = self.slider_train_test_variable,
                                                command = lambda event : self.slider_proportion(),
                                                height = 25,
                                                button_hover_color = "green",
                                                progress_color = "#4F6F52")
        
        self.slider_train_test.grid(row = 4, 
                                    column = 0,
                                    padx = 10,
                                    sticky = "WE",
                                    columnspan = 2)


        show_percent_train_test = customtkinter.CTkLabel(master = inside_frame,
                                                         textvariable = self.slider_train_test_variable)
        show_percent_train_test.grid(row = 5, 
                                     column = 0,
                                     columnspan = 2)


        valid_test_label = customtkinter.CTkLabel(master = inside_frame,
                                                  text = "Test / Validation",
                                                  font = ("Calibri light", 16))
        valid_test_label.grid(row = 6, 
                              column = 0,
                              padx = 10,
                              pady = 10,
                              sticky = "W",
                              columnspan = 2)

        self.slider_valid_test_variable = tkinter.IntVar()
        self.valid_test_slider = customtkinter.CTkSlider(master = inside_frame,
                                                         command = lambda event : print(event),
                                                         height = 25,
                                                         from_=0,
                                                         to = 100 - self.slider_train_test_variable.get(),
                                                         variable = self.slider_valid_test_variable,
                                                         button_hover_color = "green",
                                                         progress_color = "#4F6F52")
        self.valid_test_slider.grid(row = 7, 
                                    column = 0,
                                    sticky = "WE",
                                    columnspan = 2,
                                    padx = 10)
        
        self.show_percent_valid_test = customtkinter.CTkLabel(master = inside_frame, 
                                                              textvariable = self.slider_valid_test_variable)
        self.show_percent_valid_test.grid(row = 8, 
                                          column = 0,
                                          columnspan = 2)

        epoch_label = customtkinter.CTkLabel(master = inside_frame,
                                             text = "Epoch",
                                             font = ("Calibri Light", 16))
        epoch_label.grid(row = 9, 
                         column = 0,
                         sticky = "W",
                         padx = 10)
        
        

        self.entry_epoch = customtkinter.CTkEntry(master = inside_frame,
                                                  validate = "key",
                                                  validatecommand=(inside_frame.register(self.validate_entry), "%S"))
        self.entry_epoch.grid(row = 10, 
                         column = 0,
                         sticky = "WE",
                         padx = 10)

        batch_size_label = customtkinter.CTkLabel(master = inside_frame,
                                                  text = "Batch Size",
                                                  font = ("Calibri Light", 16))
        batch_size_label.grid(row = 11, 
                              column = 0,
                              stick = "W",
                              padx = 10)

        self.batch_size_entry = customtkinter.CTkEntry(master=inside_frame,
                                                  validate = "key",
                                                  validatecommand=(inside_frame.register(self.validate_entry), "%S"))
        self.batch_size_entry.grid(row = 12,
                                   column = 0,
                                   stick = "WE",
                                   padx = 10)
        
        train_button = customtkinter.CTkButton(master = inside_frame,
                                               text = "Train model",
                                               command = lambda : self.train_button_func())
        train_button.grid(row = 13,
                          column = 0,
                          columnspan = 2,
                          sticky = "W",
                          padx = 10,
                          pady = 20)
        
        revert_button = customtkinter.CTkButton(master = inside_frame,
                                                text = "Revert",
                                                command = lambda : self.revert_button_func(),
                                                fg_color = "red",
                                                text_color = "white")
        revert_button.grid(row = 14,
                           column = 0,
                           columnspan = 2,
                           sticky = "W",
                           padx = 10)
        

        

        revert_button.bind("<Enter>", command = lambda event : revert_button.configure(fg_color = "#4E0707"))
        revert_button.bind("<Leave>", command = lambda event : revert_button.configure(fg_color = "red"))
        self.folder_combo_box.bind("<<ComboboxSelected>>", command = lambda event : self._show_info())
    
    # def _show_info(self):
    #     pass
    
        
    def train_button_func(self):
        self.show_info = tkinter.Toplevel(master = self)
        self.show_info.title("คำเตือน")
        self.show_info.geometry(newGeometry = "200x200")
        self.show_info.resizable(False, False)
        self.show_info.after(2500, func = lambda : self.show_info.iconbitmap("Icon_image/nds-website-favicon-color.ico"))

        train_percent = self.slider_train_test_variable.get()
        print(f"train_percent = {train_percent}")
        test_percent = self.slider_valid_test_variable.get()
        print(f"test_percent = {test_percent}")
        valid_percent = (100 - train_percent) - test_percent
        print(f"valid_percent = {valid_percent}")
       
        txt_list = []
        img_list = []

        file_list = os.listdir(path = f"{self.folder_combo_box.get()}")


        for i in file_list:
            if i.endswith(".txt"):
                txt_list.append(i)
            elif i.endswith((".png", ".jpg")):
                print(f"{self.folder_combo_box.get()}/{os.path.splitext(i)[0]}.txt")
                if os.path.exists(path = f"{self.folder_combo_box.get()}/{os.path.splitext(i)[0]}.txt"):
                    img_list.append(i)
            else:
                pass

        txt_list = np.array(txt_list)
        img_list = np.array(img_list)

        # สร้างชุดตัวเลขเพื่อเอาไว้สุ่ม index แล้วไปสุ่มในชื่ออีกทีเพื่อแบ่ง train, test, valid
        index_array = np.arange(len(txt_list))

        train_index, test_index, valid_index = np.split(ary = index_array, 
                                                        indices_or_sections = [int(train_percent/100 * len(index_array)),
                                                                               int((train_percent/100 + test_percent/100) * len(index_array))])
        print(f"train_index = {train_index}")
        print(f"len(train_index) = {len(train_index)}")
        print(f"test_index = {test_index}")
        print(f"len(test_index) = {len(test_index)}")
        print(f"valid_index = {valid_index}")
        print(f"len(valid_index )= {len(valid_index)}")

        print(f"len = {len(train_index) + len(test_index) + len(valid_index)}")
        
        train_img_array = img_list[train_index]
        train_txt_array = txt_list[train_index]
        test_img_array = img_list[test_index]
        test_txt_array = txt_list[test_index]
        valid_img_array = img_list[valid_index]
        valid_txt_array = txt_list[valid_index]



        os.makedirs(f"{self.folder_combo_box.get()}/train/images")
        os.makedirs(f"{self.folder_combo_box.get()}/train/labels")
        os.makedirs(f"{self.folder_combo_box.get()}/test/images")
        os.makedirs(f"{self.folder_combo_box.get()}/test/labels")
        os.makedirs(f"{self.folder_combo_box.get()}/valid/images")
        os.makedirs(f"{self.folder_combo_box.get()}/valid/labels")


        # เรียกใช้ function ที่สร้างขึ้นเองคือฟัง์ชัน copy2folder
        self.copy2folder(val_array = train_img_array,
                         des = f"{self.folder_combo_box.get()}/train/images")
        self.copy2folder(val_array = train_txt_array,
                         des = f"{self.folder_combo_box.get()}/train/labels")
        self.copy2folder(val_array = test_img_array,
                         des = f"{self.folder_combo_box.get()}/test/images")
        self.copy2folder(val_array = test_txt_array,
                         des = f"{self.folder_combo_box.get()}/test/labels")
        self.copy2folder(val_array = valid_img_array,
                         des = f"{self.folder_combo_box.get()}/valid/images")
        self.copy2folder(val_array = valid_txt_array,
                         des = f"{self.folder_combo_box.get()}/valid/labels")
        

        with open(file = f"{self.folder_combo_box.get()}/data.yaml", mode = "r") as read_file:
            data = yaml.safe_load(read_file)
            print(f"data = {data}")
            data["train"] = os.path.abspath(f"{self.folder_combo_box.get()}/train/images")
            data["test"] = os.path.abspath(f"{self.folder_combo_box.get()}/test/images")
            data["val"] = os.path.abspath(f"{self.folder_combo_box.get()}/valid/images")

        with open(file = f"{self.folder_combo_box.get()}/data.yaml", mode = "w") as write_file:
            yaml.dump(data,write_file)

        self.train_model(yaml_path = f"{self.folder_combo_box.get()}/data.yaml",
                         model_type = self.model_combo_box.get(),
                         epochs = int(self.entry_epoch.get()),
                         batch_size = int(self.batch_size_entry.get()),
                         project_path = f"{self.folder_combo_box.get()}/runs")
        

    def validate_entry(self, text):
        return text.isdecimal()
    

    
    def train_model(self, yaml_path, model_type, epochs, batch_size, project_path):        
        label_info = customtkinter.CTkLabel(master = self.show_info,
                                            text = "กรุณาอย่าปิดโปรแกรม โปรแกรมกำลังทำงานอยู่ หากทำงานเสร็จหน้าต่างนี้จะปิดลงเอง",
                                            font = ("Calibri bold", 20))
        label_info.pack(side = "top",
                        padx = 5,
                        pady = 5)

        if os.path.exists(path = f"{self.folder_combo_box.get()}/{model_type}"):
            model = YOLO(model = f"{self.folder_combo_box.get()}/{model_type}")
            model.train(data = yaml_path, 
                        epochs = epochs,
                        batch = batch_size,
                        project = project_path)
        
        else:
            model = YOLO(model = model_type)
            model.train(data = yaml_path, 
                        epochs = epochs,
                        batch = batch_size,
                        project = project_path)
            shutil.move(src = f"{model_type}", dst = f"{self.folder_combo_box.get()}/{model_type}")

        self.show_info.destroy()

        tkinter.messagebox.showinfo(title = "Complete",
                                    message = "ทำการเทรนโมเดลสำเร็จแล้ว")

    
    def revert_button_func(self):
        shutil.rmtree(f"{self.folder_combo_box.get()}/train")
        shutil.rmtree(f"{self.folder_combo_box.get()}/test")
        shutil.rmtree(f"{self.folder_combo_box.get()}/valid")
        shutil.rmtree(f"{self.folder_combo_box.get()}/runs")
        # os.remove(path = f"{self.folder_combo_box.get()}/{self.model_combo_box.get()}")
        
        with open(file = f"{self.folder_combo_box.get()}/data.yaml", mode = "r") as read_file:
            data = yaml.safe_load(read_file)
            del data["train"], data["test"], data["val"]
        with open(file = f"{self.folder_combo_box.get()}/data.yaml", mode = "w") as write_file:
            yaml.dump(data, write_file)

        del read_file, write_file, data

        tkinter.messagebox.showinfo(title = "Complete",
                                    message = "ทำการ Revert เสร็จสิ้น")


    def get_folder(self):
        workspace_path = os.listdir()
        folder_list = []
        for i in workspace_path:
            if i[:6] == "Image_":
                folder_list.append(i)
            else:
                pass
        return folder_list
        

    def slider_proportion(self):
        self.valid_test_slider.configure(from_ = 0,
                                         to = 100 - self.slider_train_test_variable.get())


    def copy2folder(self, val_array, des):
        for i in val_array:
            shutil.copy2(src = f"{self.folder_combo_box.get()}/{i}",
                         dst = des)