## Import Library
import cv2
from PIL import Image, ImageTk
import tkinter
import customtkinter
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from menu import Menu_tab
import torch


## Demo App
class Main_demo(tkinter.Toplevel):
    def __init__(self, title : str, geometry : list|tuple, folder : str):
        # สืบทอดทุก method ของ customtkinter.CTk ทั้งหมด
        super().__init__()

        self.folder = folder
        self.title(string = title)
        self.geometry(f"{geometry[0]}x{geometry[1]}")
        self.resizable(width = False, height = False)
        self.columnconfigure(index = 0, weight = 5)
        self.columnconfigure(index = 1, weight = 95)


        menu_tab = Menu_tab(parent = self)
        menu_tab.pack(side = "left",
                      fill = "both")
        cap  = cv2.VideoCapture(0)
        self.video_area = tkinter.Canvas(master = self, 
                                         bg = "red")
        self.video_area.pack(side = "left",
                             fill = "both",
                             expand = True)
        self.video_area.update()
        

        print(f"Video Area = {self.video_area.winfo_height()}")
        print(f"Video Area = {self.video_area.winfo_width()}")


        self.show_video(cap = cap)
        print("test")
        # self.mainloop()



    def show_video(self, cap):

        

        ret, frame = cap.read()
        # model = YOLO(model = f"{self.folder}/yolov8n.pt")
        # results = model.predict(frame, conf = 0.5, classes = 0, imgsz = 640)
        # boxes = results[0].boxes.xyxy.tolist()
        # print(f"boxes = {boxes}")
        if ret:
            img_fromarray = Image.fromarray(cv2.cvtColor(src = frame,
                                                         code = cv2.COLOR_BGR2RGB))
            convert_image = self.resize_image_to_canvas_ratio(image_from_array = img_fromarray)
            self.video_area.create_image(0,
                                        0,
                                        image = convert_image,
                                        anchor = tkinter.NW)
            self.video_area.update()

            for i in self.video_area.winfo_children():
                        print("test2")
                        i.destroy()

            # self.video_area.create_rectangle(boxes[0][0], boxes[0][1], boxes[0][2], boxes[0][3])
            self.video_area.convert_image = convert_image
        self.after(ms = 15, func = self.show_video(cap = cap))


    def resize_image_to_canvas_ratio(self, image_from_array):
        canvas_height = self.video_area.winfo_height()
        canvas_width = self.video_area.winfo_width()
        ratio = min(canvas_height / image_from_array.height, canvas_width / image_from_array.width)

        # ปรับขนาดของภาพ
        resized_image = image_from_array.resize((canvas_width, canvas_height), Image.BICUBIC)
        
        final_image = ImageTk.PhotoImage(resized_image)

        del canvas_height, canvas_width, ratio
        return final_image
