from tkinter import *
from tkinter import ttk
import configparser

def changePrefs():
    print("Preferences Changed")

def changeDest():
    print("Destination Changed")

def organize():
    print("Files Organized")

def killProg():
    print("Goodbye")

root = Tk() #always first line other than any methods that need to be defined 

root.title("Movie Organizer")

mainframe = ttk.Frame(root, padding = "3 3 12 12")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))

root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

config = configparser.ConfigParser()

destinationFolder = StringVar('')
fieldPreferences = StringVar('')



ttk.Label(mainframe, textvariable = fieldPreferences).grid(column = 1, row = 1, sticky = W) #query preferences
ttk.Button(mainframe, text = "Change", command = changePrefs).grid(column = 3, row = 1, sticky = W) #change prefs

ttk.Label(mainframe, textvariable = destinationFolder).grid(column = 1, row = 2, sticky = W) #destination Folder
ttk.Button(mainframe, text = "Change", command = changeDest).grid(column = 3, row = 2, sticky =  W) # change dest

ttk.Button(mainframe, text = "Organize", command = organize).grid(column = 1, row = 3, sticky = W)# organize button
#add dropdown
ttk.Button(mainframe, text = "Add Profile", command = addProfile).grid(column = 3, row = 3, sticky = W) #add user profile button
ttk.Button(mainframe, text = "Exit", command = killProg).grid(column = 4, row = 3, sticky = W) #kill program button

for child in mainframe.winfo_children(): child.grid_configure(padx = 10, pady = 10)

#root.bind('<Return>', organize)  #bind the enter button to organize.

root.mainloop() #always last line
