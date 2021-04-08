import sys
import os
from tkinter import *
from tkinter import filedialog
from zipfile import ZipFile
import re

intro = "Welcome to ZipReader.\n"
intro2 = "This tool checks for hidden files in Zip Folders."
intro3 = "It lists existing files in the archive and checks for differences in the zip archive file\ndirectory and central file directory entries."
intro4 = "A mismatch can determine if there is a hidden file in the archive."
intro5 = "Press Y to continue, or another key to quit."
space = ""

#display intro statements to the user.
print(intro.title())
print(intro2.title())
print(intro3.title())
print(intro4.title())
y = input(intro5.title())
print(space)

if(y != 'Y'):
    sys.exit()

#the following code displays a gui to user allowing them to choose a zip file of there choice.
root = Tk()
root.fileName = filedialog.askopenfilename(initialdir="/", title="Zip Reader Tool",
                                           filetypes=(("zip files", "*.zip"), ("All Files", "*.*")))
print(root.fileName)

#display all unhidden files of the archive to the user and
#their respective information. Also display total archive size.
with ZipFile(root.fileName, 'r') as size:
    for info in size.infolist():
        print(info.filename)
        print("\tSystem: \t\t" + str(info.create_system))
        print("\tZip Version:\t" + str(info.create_version))
        print('\tCompressed Size:\t' + str(info.compress_size) + 'Bytes')
        print("\tUncompressed:\t" + str(info.file_size) + ' Bytes\n')

    print("\tTotal Archive Size: " + str(os.path.getsize(root.fileName)) + ' Bytes\n')

#check if zipfile is truly empty
#if so, end program.
if (os.path.getsize(root.fileName) == 0x16):
    print("\nZip File is Empty, There are no hidden files!")
    print("Have a Nice Day!")
    sys.exit()

print("Zip Reader will now check for differences between local file headers and the central directory.\nNote that 'entries' refers to file entries.")
input("Press any key to continue...")
print(space)
#find all instances of files in local file headers.
with open(root.fileName, 'rb') as binary_file:
    f1 = re.findall(b'\x50\x4b\x03\x04', binary_file.read())
    counter1 = 0
    for hex1 in f1:
        counter1 += 1

print("There are " + str(counter1) + " entries in the local file headers.") # display count of entries to user

print(space)

#find all instances of files in central file directory.
with open(root.fileName, 'rb') as centralCounter:
    f2 = re.findall(b'\x50\x4b\x01\x02', centralCounter.read())
    counter2 = 0
    for hex2 in f2:
        counter2 += 1

print("There are " + str(counter2) + " entries in the central directory file headers.") #display the amount of instances to the user.

print(space)

#count the number of differences(if any) to user. if there are differences, then there are hidden files.
counter3 = counter1 - counter2

if(counter1 != counter2):
    print("WARNING, There is a mismatch in entries between local file headers and central directory file headers.\n")
    print("Missing entries: " + str(counter3))
else:
    print("There are no hidden entries..")

#ask user to check total entries of the archive.
print("Sometimes users can edit total entries to hide files as well.")
check = input("Would you like to check total entries?Y/n")

if(check == 'Y' or check == 'y'):
    print(space)

if(check == 'n'):
    print("Thanks for using Zip Reader.")
    sys.exit()

#check the number of total entries and display them to the user.
with open(root.fileName, 'rb') as diskEntry:
    diskEntry.seek(-12, os.SEEK_END)
    entry = diskEntry.read(1)
    totalEntries = int.from_bytes(entry, byteorder='big')
    if(totalEntries < 2):
        print("There is " + str(totalEntries) + " total entry.")
    else:
        print("There are " + str(totalEntries) + " total entries.")

    if(totalEntries == counter1):
        print("The number of total entries matches the number of file entries.\nThere are no missing entries.")
    else:
        entryMiss = counter1 - totalEntries
        print("**WARNING** Missing Entries: " + str(entryMiss))

close = input("Enter 'quit' + to terminate.\n")
closemsg = ("Thank you for using Zip Reader!")
print(closemsg.title())
if (close == 'quit'):
    sys.exit()
root.mainloop()
