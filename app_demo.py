## Import Library
import cv2
from PIL import Image, ImageTk
import tkinter
import customtkinter
from ultralytics import YOLO
import pandas as pd
import os
import shutil
# from ultralytics.utils.plotting import Annotator


class Main_demo:
    def __init__(self, parent : object, folder : str):
        if folder != "Select":
            self.folder = folder
            cap = cv2.VideoCapture(0)
            top_level = tkinter.Toplevel(master = parent)
            top_level.geometry(f"{round(cap.get(3) * 2.5)}x{round(cap.get(4) * 2)}")
            top_level.resizable(width = False,
                                height = False)
            top_level.title("App Demo")
            top_level.after(ms = 250,
                            func = lambda : top_level.iconbitmap("Icon_image/nds-website-favicon-color.ico"))
            
            
            # for root, dirs, files in os.walk(f"{folder}"):
            #     for i in files:
            #         if i.lower().endswith(".pt"):
            #             model_pretrain = YOLO(f"{folder}/{i}")
            for i in os.listdir(f"{folder}"):
                if i.endswith(".pt"):
                    model_pretrain = YOLO(model = f"{folder}/{i}")
                    

            # model_pretrain = YOLO(model = f"{folder}/yolov8n.pt")
            model_aftertrain = YOLO(model = f"{folder}/runs/train/weights/best.pt")
            name_column = ["person"]
            name_column.extend(list(model_aftertrain.names.values()))
            print(f"")
            print(f"name_column = {name_column}")
            print(f"")

            self.df = pd.DataFrame({"Name." : name_column, "Count" : [0] * len(name_column)})
            print(self.df)
            r_set = self.df.to_numpy().tolist()
            

            print()
            print(f"self.df.to_numpy().tolist() = {r_set}")
            print()

            info_frame = customtkinter.CTkFrame(master = top_level)
            info_frame.pack(side = "left",
                            fill = "both",
                            padx = 10,
                            pady = 10)
            log_tab = customtkinter.CTkTabview(master = info_frame)
            log_tab.pack(side = "top",
                        fill = "both",
                        padx = 5,
                        expand = True)
            log_tab.add(name = "Log Tab")
            
            
            self.tree_view = tkinter.ttk.Treeview(master = log_tab.tab(name = "Log Tab"),
                                            columns = list(self.df.keys()),
                                            show = "headings")
            self.tree_view.pack(fill = "both",
                        expand = True)
            self.tree_view.heading("Name.", 
                            text = "Name")
            self.tree_view.heading("Count", 
                            text = "Count")
            self.tree_view.column("Count", 
                            minwidth=20, 
                            width=30)
            print()
            print(f"self.df.values = {list(self.df.values)}")
            print()


            ### Get model Button
            get_model_button = customtkinter.CTkButton(master = info_frame,
                                                       text = "Get this model! (+ Pretrain_model)",
                                                       font = ("Calibri bold", 16),
                                                       command = lambda : self.get_model_to_desktop(folder = folder))
            get_model_button.pack(side = "top",
                                  fill = "x",
                                  padx = 5,
                                  pady = 5)
            
            for i in r_set:
                self.tree_view.insert("", tkinter.END, values = i)
            
            
            
            video_area = tkinter.Canvas(master = top_level)
            video_area.pack(side = "left",
                            fill = "both",
                            expand = True)
            video_area.update()

            print(f"video_area width = {video_area.winfo_width()}")
            print(f"video_area height = {video_area.winfo_height()}")
            
            self.show_video(canvas = video_area, 
                            cap = cap, 
                            master = top_level, 
                            model_pretrain = model_pretrain,
                            model_aftertrain = model_aftertrain)


        else:
            tkinter.messagebox.showerror(title = "Error",
                                         message = "กรุณาเลือกโฟลเดอร์ที่ต้องการก่อน")
            pass
        
    def get_model_to_desktop(self, folder):
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        train_model_path = f"{folder}/runs/train/weights/best.pt"
        for i in os.listdir(f"{folder}"):
            if i.endswith(".pt"):
                pretrain_model_path = f"{folder}/{i}"
        shutil.copy2(src = train_model_path,
                     dst = desktop_path)
        shutil.copy2(src = pretrain_model_path,
                     dst = desktop_path)
        
        tkinter.messagebox.showinfo(title = "Information",
                                    message = "ทำการโหลดโมเดลของท่านเสร็จสิ้น (บน desktop)")

    def show_video(self, canvas : object, cap : object, master : object, model_pretrain : object, model_aftertrain : object):



        def update_table(dataframe : object, result_pretrain : object, result_train : object, model_pretrain : object, model_aftertrain : object):
            
            name_pretrain = model_pretrain.names
            name_aftertrain = model_aftertrain.names
            count = 0

            print()

            my_list_count1 = {name_aftertrain[int(i)]:result_train[0].boxes.cls.tolist().count(int(i)) for i in result_train[0].boxes.cls.tolist()}


            if len(result_pretrain[0].boxes.cls.tolist()) != 0:
                for i in self.tree_view.get_children():
                    for value in self.tree_view.item(i)["values"]:
                        if value == "person":
                            self.tree_view.set(i, "Count", len(result_pretrain[0].boxes.cls.tolist()))
                        else:
                            pass
            else:
                for i in self.tree_view.get_children():
                    for value in self.tree_view.item(i)["values"]:
                        if value == "person":
                            self.tree_view.set(i, "Count", 0)
                        else:
                            pass
            

            if len(results_af[0].boxes.cls.tolist()) != 0:
                for i in self.tree_view.get_children():
                    for j in my_list_count1.keys():
                        if self.tree_view.item(i)["values"][0] == j:
                            self.tree_view.set(i, "Count", my_list_count1[j])
                        else:
                            pass
            else:
                for i in self.tree_view.get_children():
                    if i != "I001":
                        self.tree_view.set(i, "Count", 0)

                # list(set(result_train[0].boxes.cls.tolist()))
            
            # df_train = pd.DataFrame({"Name" : name_aftertrain, "Count" : [].extend()})
            


            # if len(results_af[0].boxes.cls.tolist()) != 0:
            #     for i in results_af[0].boxes.cls.tolist():

            #         # for j in self.tree_view.get_children():
            #         #     if name_aftertrain[int(i)] == self.tree_view.item(j)["values"][0]:
                            
            #         #         for k in results_af[0].boxes.cls.tolist():
            #         #             if k == self.tree_view.item(j)["values"][0]:
            #         #                 count += 1
            #         #         self.tree_view.set(j, "Count", count)
            #         #     else:
            #         #         self.tree_view.set(j, "Count", self.tree_view.item(j)["values"][1])

            # else:
            #     for i in self.tree_view.get_children():
            #         if i != "I001":
            #             self.tree_view.set(i, "Count", 0)
            
            # if len(result_train[0].boxes.cls.tolist()) != 0:
            #     for i in result_train[0].boxes.cls.tolist():
            #         for j in self.tree_view.get_children():
            #             print(f"j = {j}")
            #             for value in self.tree_view.item(j)["values"]:
            #                 print(f"self.tree_view.item(j) = {self.tree_view.item(j)}")
            #                 if value == name_aftertrain[int(i)]:
            #                     self.tree_view.item(j)["values"][1] = self.tree_view.item(j)["values"][1] + 1
            #                     self.tree_view.set(j, "Count", self.tree_view.item(j)["values"][1])
            #                 else:
            #                     self.tree_view.item(j)["values"][1] = self.tree_view.item(j)["values"][1] 
            #                     self.tree_view.set(j, "Count", self.tree_view.item(j)["values"][1])
            
            # else:
            #     for i in self.tree_view.get_children():
            #         for value in self.tree_view.item(i)["values"]:
            #             print(f"self.tree_view.item(i) = {self.tree_view.item(i)}")
            #             if value == name_aftertrain[int()]:
            #                 self.tree_view.item(j)["values"][1] = 0

            
            

    
        ret, frame = cap.read()

        # ผ่าน blur
        frame = cv2.GaussianBlur(src = frame,
                        ksize = (3, 3),
                        sigmaX = 0)

        if ret:
            # predict แค่ คนเท่านั้น
            results = model_pretrain.predict(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 
                                                        classes = [0])

            results_af = model_aftertrain.predict(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            names = model_pretrain.names
            names_af = model_aftertrain.names

            print(f"")
            print(f"results[0].boxes.xyxy.tolist() = {results[0].boxes.xyxy.tolist()}")
            print(f"")
            print(f"")
            print(f"results_af[0].boxes.xyxy.tolist() = {results_af[0].boxes.xyxy.tolist()}")
            print(f"")
            print(f"")
            
            

            if len(results_af[0].boxes.xyxy.tolist()) == 0:
                zip_element = zip(results[0].boxes.xyxy.tolist(), 
                                results[0].boxes.cls.tolist(), 
                                results[0].boxes.conf.tolist())
                for xyxy_pre, cls_pre, conf_pre  in zip_element:

                    cv2.rectangle(img = frame, 
                                pt1 = (int(xyxy_pre[0]), int(xyxy_pre[1])), 
                                pt2 = (int(xyxy_pre[2]), int(xyxy_pre[3])), 
                                color = (255,0,0),
                                thickness = 2)

                    

                    cv2.putText(img = frame,
                                org = (int(xyxy_pre[0]), int(xyxy_pre[1])-5),
                                text = f"class = {names[int(cls_pre)]}, prob = {round(conf_pre, 2)}",
                                fontScale = 0.5,
                                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                                thickness = 1,
                                color = (255, 0, 0))
            

            else:
                zip_element = zip(results[0].boxes.xyxy.tolist(), 
                                results[0].boxes.cls.tolist(), 
                                results[0].boxes.conf.tolist(), 
                                results_af[0].boxes.xyxy.tolist(), 
                                results_af[0].boxes.cls.tolist(), 
                                results_af[0].boxes.conf.tolist())
                
                for xyxy_pre, cls_pre, conf_pre, xyxy_af, cls_af, conf_af  in zip_element:

                    cv2.rectangle(img = frame, 
                                pt1 = (int(xyxy_pre[0]), int(xyxy_pre[1])), 
                                pt2 = (int(xyxy_pre[2]), int(xyxy_pre[3])), 
                                color = (255,0,0),
                                thickness = 2)
                    cv2.rectangle(img = frame, 
                                pt1 = (int(xyxy_af[0]), int(xyxy_af[1])), 
                                pt2 = (int(xyxy_af[2]), int(xyxy_af[3])), 
                                color = (0,0,255),
                                thickness = 2)
                    

                    cv2.putText(img = frame,
                                org = (int(xyxy_pre[0]), int(xyxy_pre[1])-5),
                                text = f"class = {names[int(cls_pre)]}, prob = {round(conf_pre, 2)}",
                                fontScale = 0.5,
                                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                                thickness = 1,
                                color = (255, 0, 0))
                    cv2.putText(img = frame,
                                org = (int(xyxy_af[0]), int(xyxy_af[1])-5),
                                text = f"class = {names_af[int(cls_af)]}, prob = {round(conf_af, 2)}",
                                fontScale = 0.5,
                                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                                thickness = 1,
                                color = (0, 0, 255))
                
            
            image = Image.fromarray(obj =  cv2.cvtColor(src = frame, code = cv2.COLOR_BGR2RGB))
                
            ratio = min(canvas.winfo_width()/image.width, 
                        canvas.winfo_height()/image.height)


            print(f"ratio = {ratio}")
            
            new_width = int(image.width * ratio)
            new_height = int(image.height * ratio)

            photo = ImageTk.PhotoImage(image.resize((new_width, new_height), Image.BICUBIC))
            canvas.create_image(0,
                                0,
                                image = photo,
                                anchor = tkinter.NW)
            canvas.image = photo
            
            update_table(dataframe = self.df,
                        result_pretrain = results,
                        result_train = results_af,
                        model_aftertrain = model_aftertrain,
                        model_pretrain = model_pretrain)
            
            master.after(15, func = lambda : self.show_video(canvas = canvas,
                                                            cap = cap,
                                                            master = master,
                                                            model_pretrain = model_pretrain,
                                                            model_aftertrain = model_aftertrain))

                

            
        

