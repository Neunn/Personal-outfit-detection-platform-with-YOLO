import os

for i in os.listdir():
    if i[:6] == "Image_":
        print(i)
