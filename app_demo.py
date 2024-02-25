## Import Library
import cv2
from PIL import Image, ImageTk
import tkinter
import customtkinter
from ultralytics import YOLO
import pandas as pd
import numpy as np
# from ultralytics.utils.plotting import Annotator


class Main_demo:
    def __init__(self, parent : object, folder : str):

        self.folder = folder
        cap = cv2.VideoCapture(0)
        top_level = tkinter.Toplevel(master = parent)
        top_level.geometry(f"{round(cap.get(3) * 2.5)}x{round(cap.get(4) * 2)}")
        top_level.resizable(width = False,
                            height = False)
        top_level.title("App Demo")
        top_level.after(ms = 250,
                        func = lambda : top_level.iconbitmap("Icon_image/nds-website-favicon-color.ico"))
        
        

        model_pretrain = YOLO(model = f"{folder}/yolov8n.pt")
        model_aftertrain = YOLO(model = f"{folder}/runs/train/weights/best.pt")
        name_column = ["person"]
        name_column.extend(list(model_aftertrain.names.values()))
        print(f"")
        print(f"name_column = {name_column}")
        print(f"")

        df = pd.DataFrame({"Name." : name_column, "Count" : [0] * len(name_column)})
        print(df)
        r_set = df.to_numpy().tolist()
        

        print()
        print(f"df.to_numpy().tolist() = {r_set}")
        print()


        log_tab = customtkinter.CTkTabview(master = top_level)
        log_tab.pack(side = "left",
                     fill = "both",
                     padx = 10)
        log_tab.add(name = "treeview_tab")
        
        
        self.tree_view = tkinter.ttk.Treeview(master = log_tab.tab(name = "treeview_tab"),
                                         columns = list(df.keys()),
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
        print(f"df.values = {list(df.values)}")
        print()

        
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
        



    def show_video(self, canvas : object, cap : object, master : object, model_pretrain : object, model_aftertrain : object):
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

            
            master.after(15, func = lambda : self.show_video(canvas = canvas,
                                                             cap = cap,
                                                             master = master,
                                                             model_pretrain = model_pretrain,
                                                             model_aftertrain = model_aftertrain))
            

            # master.after(15, func = lambda : self.update_table(results = results,
            #                                                    results_af = results_af,
            #                                                    model_pretrain = model_pretrain,
            #                                                    model_train = model_aftertrain,
            #                                                    treeview = self.tree_view))

        else:
            tkinter.messagebox.showerror(title = "error",
                                         message = "เกิดข้อผิดพลาดขึ้นขณะกำลังทำงาน")

        
    
        def update_table(dataframe : object, result_pretrain : object, result_train : object):
            pass
