import tkinter as tk
from tkinter import ttk, filedialog
import os
from zipfile import ZipFile
from PIL import Image, ImageTk
import cv2

class ImageLabelingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Labeling Tool")

        self.image_folder = ""
        self.class_list = []

        self.create_widgets()

    def create_widgets(self):
        # Frame for file input
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=10)

        ttk.Label(file_frame, text="Select .zip file:").grid(row=0, column=0, padx=5, pady=5)
        self.zip_file_entry = ttk.Entry(file_frame, width=30)
        self.zip_file_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_zip_file).grid(row=0, column=2, padx=5, pady=5)

        # Treeview for displaying image list
        self.tree = ttk.Treeview(self.root, columns=('Image'))
        self.tree.heading('#0', text='File Name')
        self.tree.column('#0', width=200)
        self.tree.pack(expand=True, fill='both')

        # Binding function to treeview item selection
        self.tree.bind('<ButtonRelease-1>', self.show_image)

        # Class selection frame
        class_frame = ttk.Frame(self.root)
        class_frame.pack(pady=10)

        ttk.Label(class_frame, text="Select class:").grid(row=0, column=0, padx=5, pady=5)
        self.class_entry = ttk.Entry(class_frame, width=20)
        self.class_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(class_frame, text="Add Class", command=self.add_class).grid(row=0, column=2, padx=5, pady=5)

        # Labeling button
        ttk.Button(self.root, text="Export Labels", command=self.export_labels).pack(pady=10)

    def browse_zip_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
        self.zip_file_entry.delete(0, tk.END)
        self.zip_file_entry.insert(0, file_path)

        # Extract images from zip file and update treeview
        self.extract_images(file_path)

    def extract_images(self, zip_file_path):
        with ZipFile(zip_file_path, 'r') as zip_ref:
            # Extract all contents of zip file to a folder
            self.image_folder = os.path.join(os.path.dirname(zip_file_path), "extracted_images")
            zip_ref.extractall(self.image_folder)

        # Update treeview with image files
        self.update_treeview()

    def update_treeview(self):
        # Clear existing items in treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add images to treeview
        for root, dirs, files in os.walk(self.image_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    self.tree.insert('', 'end', values=(file,))

    def show_image(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            selected_image_path = os.path.join(self.image_folder, self.tree.item(selected_item, 'values')[0])

            # Display the selected image in a separate window
            image = Image.open(selected_image_path)
            image = image.resize((400, 400))  # Resize the image as needed
            tk_image = ImageTk.PhotoImage(image)

            image_window = tk.Toplevel(self.root)
            image_label = tk.Label(image_window, image=tk_image)
            image_label.pack()

            image_window.mainloop()

    def add_class(self):
        class_name = self.class_entry.get()
        if class_name and class_name not in self.class_list:
            self.class_list.append(class_name)
            self.class_entry.delete(0, tk.END)
            print(f"Class '{class_name}' added.")

    def export_labels(self):
        # Create a YOLOv8 format label file
        label_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        with open(label_file_path, 'w') as label_file:
            # Iterate through labeled images and write YOLOv8 format labels
            for root, dirs, files in os.walk(self.image_folder):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        image_path = os.path.join(root, file)
                        # Extract coordinates and class labels from your labeling mechanism
                        x_min, y_min, x_max, y_max = 0, 0, 100, 100  # Replace with actual coordinates
                        class_label = "class_label"  # Replace with actual class label

                        label_file.write(f"{class_label} {x_min} {y_min} {x_max} {y_max}\n")

        print(f"Labels exported to: {label_file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageLabelingApp(root)
    root.mainloop()
