import os
from asyncio.windows_events import NULL
from os import mkdir

path = input("Enter the path of the folder you want to organize & store : ")

dir_elements = []

file_categories = {
    ".png": "Images",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".webp": "Images",

    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",

    ".mp3": "Audio",
    ".m4a": "Audio",
    ".wav": "Audio",

    ".mp4": "Videos",
    ".mkv": "Videos"
}

if os.path.isdir(path) :
    print("\nValid path\n")
    dir_elements = os.listdir(path)

else:
    print("Invalid path")

for element in dir_elements:
    full_path = os.path.join(path, element)

    if os.path.isfile(full_path) :
        filename,extension = (os.path.splitext(element))

        category = file_categories.get(extension.lower(),"Others")

        if category == "Images" and ImgPath == NULL :
            os.mkdir(category)
        elif category == "Images" :
            ImgPath = os.path.join(path, category)
            print(ImgPath)
        elif category == "Audio" :
            AudioPath = os.path.join(path,category)
            print(AudioPath)
        elif category == "Documents" :
            docPath = os.path.join(path,category)
            print(docPath)
    else:
        print(element,"is a Folder")

    
