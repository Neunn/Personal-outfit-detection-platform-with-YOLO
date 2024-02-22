## Import Library
import cv2
from PIL import Image, ImageTk
import tkinter
import customtkinter
from ultralytics import YOLO
# from ultralytics.utils.plotting import Annotator


class Main_demo:
    def __init__(self, parent : object, folder : str):

        self.folder = folder
        top_level = tkinter.Toplevel(master = parent)
        top_level.geometry("1600x800")
        top_level.resizable(width = False,
                                 height = False)
        top_level.title("App Demo")
        top_level.columnconfigure(index = 0,
                                  weight = 5)
        top_level.columnconfigure(index = 1,
                                  weight = 95)
        
        model_pretrain = YOLO(model = f"{folder}/yolov8n.pt")
        model_aftertrain = YOLO(model = f"{folder}/runs/train/weights/best.pt")
        menu_tab = Menu_tab(parent = top_level)
        menu_tab.pack(side = "left",
                      fill = "both",
                      padx = 5,
                      pady = 10)
        
        video_area = tkinter.Canvas(master = top_level)
        video_area.pack(side = "left",
                        fill = "both",
                        expand = True)
        video_area.update()

        print(f"video_area width = {video_area.winfo_width()}")
        print(f"video_area height = {video_area.winfo_height()}")
        
        cap = cv2.VideoCapture(0)
        self.show_video(canvas = video_area, 
                        cap = cap, 
                        master = top_level, 
                        model_pretrain = model_pretrain,
                        model_aftertrain = model_aftertrain)
        top_level.mainloop()


    def show_video(self, canvas : object, cap : object, master : object, model_pretrain : object, model_aftertrain : object):
        ret, frame = cap.read()
        
        if ret:
            # predict แค่ คนเท่านั้น
            results = model_pretrain.predict(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), 
                                                          classes = [0])
            results_af = model_aftertrain.predict(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            names = model_pretrain.names
            names_af = model_aftertrain.names

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
            
            print(f"results[0].boxes.xyxy.tolist() = {results[0].boxes.xyxy.tolist()}")
            print(f"results_af[0].boxes.xyxy.tolist() = {results_af[0].boxes.xyxy.tolist()}")



                

                
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

        else:
            tkinter.messagebox.showerror(title = "error",
                                         message = "เกิดข้อผิดพลาดขึ้นขณะกำลังทำงาน")
            cap.release()


        
            

            
            
            

        

class Menu_tab(customtkinter.CTkTabview):
    def __init__(self, parent):
        super().__init__(master = parent)

        ## Tabs
        self.add("Detection")
        self.add("Log")

        ## Widget   
        detection_frame = Detection_Frame(self.tab("Detection"))
        log_frame = Log_Frame(self.tab("Log"))
        

class Detection_Frame(customtkinter.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = "red")
        self.pack(expand = True, fill = "both")


        
class Log_Frame(customtkinter.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master = parent, fg_color = "blue")
        self.pack(expand = True, fill = "both")

        