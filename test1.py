import tkinter as tk
import cv2
from PIL import Image, ImageTk

class VideoPlayerApp:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Video Player")

        self.cap = cv2.VideoCapture(0)

        self.canvas = tk.Canvas(parent)
        self.canvas.pack()

        self.show_video()

    def show_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            canvas_height = self.canvas.winfo_reqheight()
            canvas_width = self.canvas.winfo_reqwidth()
            ratio = min(canvas_height / frame.height, canvas_width / frame.width)

            new_width = int(frame.width * ratio)
            new_height = int(frame.height * ratio)

            # ปรับขนาดของภาพ
            resized_image = frame.resize((new_width, new_height), Image.BICUBIC)
            

            photo = ImageTk.PhotoImage(image=frame)
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.photo = photo  # เก็บอ็อบเจ็กต์ PhotoImage เพื่อป้องกันการ garbage collected

        self.parent.after(5, self.show_video)

# สร้างหน้าต่าง Tkinter
root = tk.Tk()
# สร้าง Toplevel
toplevel = tk.Toplevel(root)

# สร้างแอปพลิเคชันวิดีโอและเริ่มการทำงาน
app = VideoPlayerApp(toplevel)

root.mainloop()
