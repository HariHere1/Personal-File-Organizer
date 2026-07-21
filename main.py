import os
import shutil
import sys
import time

print("=====================================\n\tPERSONAL FILE ORGANIZER\n=====================================")
folder_path = input("\nEnter the path of the folder you want to organize & store : ")


file_categories = {
    ".png": "Images",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".webp": "Images",
    ".mov": "Videos",

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

if os.path.isdir(folder_path):
    print("\n\u2713Valid path\n")
    dir_elements = os.listdir(folder_path)

    time.sleep(2)
else:
    print("\nInvalid path")
    sys.exit()

for element in dir_elements:
    source_file_path = os.path.join(folder_path, element)

    if os.path.isfile(source_file_path):
        filename, extension = (os.path.splitext(element))

        category = file_categories.get(extension.lower(), "Others")

        dest_path = os.path.join(folder_path, category)

        target_file_path = os.path.join(dest_path, element)

        if not os.path.isdir(dest_path):
            os.mkdir(dest_path)
            shutil.move(source_file_path, target_file_path)
            time.sleep(1)
            print("\n")
            print("Moving", element, "to", category)

        else:
            shutil.move(source_file_path, target_file_path)
            time.sleep(1)
            print("\n")
            print("Moving", element, "to", category)
    else:
        time.sleep(1)
        print("\n")
        print(element, "is a Folder")

