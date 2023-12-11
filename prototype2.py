import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageLabelingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Labeling Tool")
        
        # สร้างข้อมูลที่ใช้เก็บ bounding box
        self.bbox_data = []
        
        # สร้าง Canvas สำหรับแสดงรูปภาพ
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)
        
        # เพิ่มปุ่มสำหรับเลือกรูปภาพ
        self.select_image_button = tk.Button(root, text="Select Image", command=self.load_image)
        self.select_image_button.pack(side="top")
        
        # เพิ่มปุ่มสำหรับ export ข้อมูล
        self.export_button = tk.Button(root, text="Export Data", command=self.export_data)
        self.export_button.pack(side="bottom")
        
        # ผูกเหตุการณ์คลิกที่ Canvas
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # ตัวแปรสำหรับการลากเลือก
        self.start_x = 0
        self.start_y = 0
        self.rect = None
        self.img_tk = None
    
    def load_image(self):
        # เปิดหน้าต่างสำหรับเลือกรูปภาพ
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        
        if file_path:
            # โหลดรูปภาพและปรับขนาดลงที่ตำแหน่งที่ต้องการ
            image = Image.open(file_path)
            
            # คำนวณขนาดที่คงสัดส่วน
            target_width = 1000  # ขนาดที่ต้องการ
            ratio = target_width / float(image.width)
            target_height = int(ratio * float(image.height))
            
            # ปรับขนาด
            resized_image = image.resize((target_width, target_height), Image.ANTIALIAS)
            
            # แสดงรูปภาพบน Canvas
            self.img_tk = ImageTk.PhotoImage(resized_image)
            self.canvas.config(width=self.img_tk.width(), height=self.img_tk.height())
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
            
            # ล้างข้อมูล bounding box เก่า
            self.bbox_data = []
    
    def on_press(self, event):
        # เก็บตำแหน่งเริ่มต้นของการลากเลือก
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        
        # สร้างกล่องสี่เหลี่ยมเริ่มต้น
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", tags="current_rect")
    
    def on_drag(self, event):
        # ปรับปรุงขนาดของกล่องสี่เหลี่ยมขณะลาก
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords("current_rect", self.start_x, self.start_y, cur_x, cur_y)
    
    def on_release(self, event):
        # เก็บข้อมูล bounding box เมื่อปล่อยเมาส์
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        bbox = (min(self.start_x, end_x), min(self.start_y, end_y), max(self.start_x, end_x), max(self.start_y, end_y))
        self.bbox_data.append(bbox)
        
        # ลบกล่องสี่เหลี่ยม
        self.canvas.delete("current_rect")
    
    def export_data(self):
        # สร้างไฟล์ข้อมูลสำหรับเทรน YOLO
        output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        
        if output_file_path:
            with open(output_file_path, "w") as f:
                for bbox in self.bbox_data:
                    # คำนวณค่า normalized coordinates สำหรับ YOLO
                    width, height = self.img_tk.width(), self.img_tk.height()
                    x_center = (bbox[0] + bbox[2]) / (2 * width)
                    y_center = (bbox[1] + bbox[3]) / (2 * height)
                    box_width = (bbox[2] - bbox[0]) / width
                    box_height = (bbox[3] - bbox[1]) / height
                    
                    # เขียนข้อมูล bounding box ลงในไฟล์
                    line = f"0 {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n"
                    f.write(line)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageLabelingApp(root)
    root.mainloop()
