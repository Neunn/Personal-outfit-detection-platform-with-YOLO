import tkinter as tk
from tkinter import ttk
from ultralytics import YOLO


# กำหนดค่าเริ่มต้น
epochs = 100
batch_size = 32

# สร้างหน้าต่างหลัก
window = tk.Tk()
window.title("YOLOv8 Training Progress")

# สร้างป้ายชื่อ
label_epochs = tk.Label(text="Epochs:")
label_epochs.pack()

# สร้างแถบเลื่อนสำหรับจำนวน epoch
epoch_slider = tk.Scale(window, from_=1, to=200, orient=tk.HORIZONTAL, value=epochs)
epoch_slider.pack()

# สร้างป้ายชื่อ
label_batch_size = tk.Label(text="Batch Size:")
label_batch_size.pack()

# สร้างแถบเลื่อนสำหรับขนาดชุดข้อมูล
batch_size_slider = tk.Scale(window, from_=1, to=64, orient=tk.HORIZONTAL, value=batch_size)
batch_size_slider.pack()

# สร้างปุ่มเริ่มต้นการฝึกอบรม
button_start_training = tk.Button(text="Start Training")
button_start_training.pack()

# สร้างแถบความคืบหน้า
progress_bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, mode='determinate', length=200)
progress_bar.pack()

# ฟังก์ชันสำหรับเริ่มต้นการฝึกอบรม
def start_training():
    # รับค่าจากแถบเลื่อน
    epochs = epoch_slider.get()
    batch_size = batch_size_slider.get()

    # เริ่มต้นการฝึกอบรมโมเดล YOLOv8
    model = YOLO("yolov8n.pt")
    model.train(data = r"C:\Users\ExpertBook\Desktop\WorkSpace\University\Year 3\เทอม 2\PRE-PROJECT\WorkSpace\Image_1\data.yaml",
                epochs = epochs,
                batch = batch_size)


    # อัปเดตแถบความคืบหน้า
    for epoch in range(epochs):
        progress_bar.step()
        window.update()

# กำหนดเหตุการณ์คลิกสำหรับปุ่มเริ่มต้นการฝึกอบรม
button_start_training.config(command=start_training)

# เรียกใช้mainloop() เพื่อแสดงหน้าต่าง
window.mainloop()
