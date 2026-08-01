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

    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",

    ".mp3": "Audio",
    ".m4a": "Audio",
    ".wav": "Audio",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos"
}

category_counts = {}

if os.path.isdir(folder_path):
    print("\n\u2713 Valid path\n")
    dir_elements = os.listdir(folder_path)
    time.sleep(2)
else:
    print("\nInvalid path")
    sys.exit()

for element in dir_elements:
    source_file_path = os.path.join(folder_path, element)

    if os.path.isfile(source_file_path):
        filename, extension = os.path.splitext(element)
        category = file_categories.get(extension.lower(), "Others")

        dest_path = os.path.join(folder_path, category)
        target_file_path = os.path.join(dest_path, element)

        # Duplicate handling
        count = 1
        while os.path.exists(target_file_path):
            new_filename = f"{filename} ({count}){extension}"
            target_file_path = os.path.join(dest_path, new_filename)
            count += 1

        # Create category folder if missing
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)

        # Move file
        shutil.move(source_file_path, target_file_path)
        category_counts[category] = category_counts.get(category,0) + 1
        time.sleep(1)

        # Print movement message
        final_filename = os.path.basename(target_file_path)
        if final_filename != element:
            print(f"Moving {element} (renamed to {final_filename}) to {category}")
        else:
            print(f"Moving {element} to {category}")

    else:
        time.sleep(1)
        print(f"{element} is a Folder")

print("\n--- Organization Summary ---")

for category_name,file_count in category_counts.items():
    print(f"\n{category_name}: {file_count}")
