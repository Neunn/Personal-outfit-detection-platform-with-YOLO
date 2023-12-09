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
        self.canvas.bind("<Button-1>", self.on_click)
        
    def load_image(self):
        # เปิดหน้าต่างสำหรับเลือกรูปภาพ
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        
        if file_path:
            # โหลดรูปภาพและแสดงบน Canvas
            image = Image.open(file_path)
            self.img_tk = ImageTk.PhotoImage(image)
            self.canvas.config(width=self.img_tk.width(), height=self.img_tk.height())
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
            
            # ล้างข้อมูล bounding box เก่า
            self.bbox_data = []
    
    def on_click(self, event):
        # เพิ่มข้อมูล bounding box เมื่อคลิกที่ Canvas
        x, y = event.x, event.y
        bbox = (x, y, x + 50, y + 50)  # ตัวอย่าง bounding box ขนาด 50x50
        self.bbox_data.append(bbox)
        
        # วาด bounding box บน Canvas
        self.canvas.create_rectangle(bbox, outline="red")
    
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
