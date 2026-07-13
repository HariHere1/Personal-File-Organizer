import os

path = input("Enter the path of the folder you want to organize & store : ")

if os.path.isdir(path)== True:
    print("Valid path")

else:
    print("Invalid path")