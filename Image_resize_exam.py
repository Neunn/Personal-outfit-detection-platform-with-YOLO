import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageViewerCanvas:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer with Canvas")

        # สร้าง Canvas
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        # สร้างปุ่มและแท็บต่าง ๆ
        self.btn_load_image = tk.Button(root, text="Load Image", command=self.load_image)
        self.btn_load_image.pack(pady=10)

        # ตัวแปรเก็บข้อมูลภาพ
        self.image_path = ""
        self.image = None
        self.photo = None  # ใช้เก็บข้อมูลรูปภาพสำหรับการแสดงผลใน Canvas

    def load_image(self):
        # เปิดหน้าต่างให้เลือกรูปภาพ
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png")])

        # โหลดภาพและปรับขนาดให้สัดส่วนถูกต้อง
        if self.image_path:
            original_image = Image.open(self.image_path)

            # ปรับขนาดให้สัดส่วนถูกต้องกับ Canvas
            canvas_width = self.canvas.winfo_reqwidth()
            canvas_height = self.canvas.winfo_reqheight()
            ratio = min(canvas_width / original_image.width, canvas_height / original_image.height)
            new_width = int(original_image.width * ratio)
            new_height = int(original_image.height * ratio)

            # ปรับขนาดของภาพ
            resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(resized_image)

            # ลบภาพเก่า (ถ้ามี)
            self.canvas.delete("all")

            # แสดงรูปภาพใน Canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerCanvas(root)
    root.mainloop()
