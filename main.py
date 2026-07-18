import os

path = input("Enter the path of the folder you want to organize & store : ")

dir_elements = []

if os.path.isdir(path) :
    print("\nValid path\n")
    dir_elements = os.listdir(path)

else:
    print("Invalid path")

for element in dir_elements:
    full_path = os.path.join(path, element)
    if os.path.isfile(full_path) :
        filename,extension = (os.path.splitext(element))
        print(filename, "->", extension)
    else:
        print(element,"is a Folder")


