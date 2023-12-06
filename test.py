import os
import zipfile
from tkinter import *
from tkinter import filedialog

def open_zip_file():
    file_path = filedialog.askopenfilename(filetypes=[("Zip Files", "*.zip")])

    if not file_path:
        return

    # Extract files to the 'Image' folder
    folder_name = "Image"
    counter = 1
    while os.path.exists(folder_name):
        folder_name = f"Image_{counter}"
        counter += 1
    os.makedirs(folder_name)

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(folder_name)

    print(f"Successfully extracted to {folder_name}")

root = Tk()
root.title("Zip File Extractor")

frame = Frame(root)
frame.pack(padx=20, pady=20)

open_file_button = Button(frame, text="Open Zip File", command=open_zip_file)
open_file_button.pack()

root.mainloop()