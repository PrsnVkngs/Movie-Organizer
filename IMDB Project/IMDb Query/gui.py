# remember to remove makeGUI call at the bottom when done
import configparser
from tkinter import *
from tkinter import filedialog as files
from tkinter import ttk
import gc
import os
import shutil

from get_functions import *

# title, release date, runtime, director, starrating, mpaarating, cast, plot, genre
noFields = 9
prefs = ['true'] * noFields
prefName = ['Title', 'Release date', 'Runtime', 'Director', 'Star Rating', 'MPAA Rating', 'Cast', 'Plot', 'Genre']

config_names = ['fieldprefs', 'srcfolder', 'destfolder']

config = configparser.ConfigParser()
config.read('user_preferences.ini')

source_directory = ''
destination_directory = ''

def getProfiles(cfg):
    return cfg.sections()


profiles = getProfiles(config)
defaultStartup = config[profiles[0]]['defaultprofile']
defaultStartup = str(defaultStartup)
profiles = profiles[1:]

#file mamangement functions

def detect_directory(directory, desired):
    contents = os.listdir(directory)
    is_present = False
    for each in contents:
        if(each == desired):
            is_present = True
            break
    return is_present

def get_movie_data(data, movie):
    #tmp_data =
    print('wip')

#end file management functions

def close_window(window):
    window.destroy()
    gc.collect()


def changePrefs(parent, titlePref, releasePref, runtimePref, directorPref, starRatingPref, mpaaRatingPref, castPref, plotPref, fieldPrefs, genrePref, selectedProfile):
    prefsWindow = Toplevel(parent)
    prefsWindow.title("Select new search preferences")
    prefFrame = ttk.Frame(prefsWindow, padding="5 5 15 15")
    prefFrame.grid(column=0, row=0, sticky=(N, W, E, S))

    prefsWindow.columnconfigure(0, weight=1)
    prefsWindow.rowconfigure(0, weight=1)

    ttk.Checkbutton(prefFrame, text='Title', command=lambda: updatePrefs(0, titlePref.get()), variable=titlePref,
                    onvalue='true', offvalue='false').grid(column=1, row=1, sticky=W)
    ttk.Checkbutton(prefFrame, text='Release Date', command=lambda: updatePrefs(1, releasePref.get()),
                    variable=releasePref, onvalue='true', offvalue='false').grid(column=2, row=1, sticky=W)
    ttk.Checkbutton(prefFrame, text='Runtime', command=lambda: updatePrefs(2, runtimePref.get()), variable=runtimePref,
                    onvalue='true', offvalue='false').grid(column=3, row=1, sticky=W)
    ttk.Checkbutton(prefFrame, text='Directors', command=lambda: updatePrefs(3, directorPref.get()),
                    variable=directorPref, onvalue='true', offvalue='false').grid(column=1, row=2, sticky=W)
    ttk.Checkbutton(prefFrame, text='Star Rating', command=lambda: updatePrefs(4, starRatingPref.get()),
                    variable=starRatingPref, onvalue='true', offvalue='false').grid(column=2, row=2, sticky=W)
    ttk.Checkbutton(prefFrame, text='MPAA Rating', command=lambda: updatePrefs(5, mpaaRatingPref.get()),
                    variable=mpaaRatingPref, onvalue='true', offvalue='false').grid(column=3, row=2, sticky=W)
    ttk.Checkbutton(prefFrame, text='Cast', command=lambda: updatePrefs(6, castPref.get()), variable=castPref,
                    onvalue='true', offvalue='false').grid(column=1, row=3, sticky=W)
    ttk.Checkbutton(prefFrame, text='Plot', command=lambda: updatePrefs(7, plotPref.get()), variable=plotPref,
                    onvalue='true', offvalue='false').grid(column=2, row=3, sticky=W)
    ttk.Checkbutton(prefFrame, text = 'Genre', command = lambda: updatePrefs(8, genrePref.get()), variable = genrePref,
                    onvalue = 'true', offvalue = 'false').grid(column = 3, row = 3, sticky = W)
    
    ttk.Button(prefFrame, text='Confirm', command=lambda: push_field_INI(fieldPrefs, selectedProfile)).grid(column=2, row=4,
                                                                                                     sticky=W)
    ttk.Button(prefFrame, text='Close Window', command=lambda: close_window(prefsWindow)).grid(column=3, row=4, sticky=W)
    # lf = ttk.Labelframe(prefsWindow, text = "Select the data you would like to be retrieved")
    
    for child in prefFrame.winfo_children(): child.grid_configure(padx=8, pady=8)

    print("Preferences Changed")


def push_field_INI(fields, slctdProf):
    
    preferences = []
    for boo in range(noFields):
        if prefs[boo] == 'true':
            temp = ' ' + prefName[boo] + ' '
            preferences.append(temp)

    fields.set(preferences)

    if slctdProf == 0:
        print('Add a new profile or select a different one to push to ini, as Default is selected.')
    else:
        currentProf = profiles[slctdProf]
        #config[str(currentProf)][str('destFolder'+str(slctdProf))]
        config[str(currentProf)][str('fieldPrefs'+str(slctdProf))] = str(preferences)
        print(str(preferences))

    with open('user_preferences.ini', 'w') as writeconfig:
        config.write(writeconfig)

    print('INI File Updated')


def updatePrefs(prefNo, value):
    prefs[prefNo] = value

def push_src_INI(src):
    new_src = src

def push_dst_INI(dst):
    new_dst = dst

def changeSrc(parent, new_label, gui_label):
    change_source_window = Toplevel(parent)
    change_source_window.title("Select new source directory")
    src_frame = ttk.Frame(change_source_window, padding="5 5 15 15")
    src_frame.grid(column=0, row=0, sticky=(N, W, E, S))

    change_source_window.columnconfigure(0, weight=1)
    change_source_window.rowconfigure(0, weight=1)

    ttk.Label(src_frame, text = "Selected Directory:").grid(row = 1, column  = 1, sticky = W) 
    directiontext = ttk.Label(src_frame, textvariable = new_label).grid(row = 1, column = 2, sticky = W)

    def prompt_directory():
        source_directory = files.askdirectory()
        print(source_directory)
        new_label.set(source_directory)
        change_source_window.lift()
    
    change_src_button = ttk.Button(src_frame, text = "Browse", command = prompt_directory).grid(row = 1, column = 3, sticky = W)

    def confirm_dialogue():
        gui_label.set(new_label.get())
        close_window(change_source_window)
    
    confirm_button = ttk.Button(src_frame, text = "Confirm", command = confirm_dialogue).grid(row = 1, column = 4, sticky = W)

    for child in src_frame.winfo_children(): child.grid_configure(padx=8, pady=8)
    
    print("Source Changed")


def changeDest(parent, new_label, gui_label):
    change_destination_window = Toplevel(parent)
    change_destination_window.title("Select new destination folder")
    dst_frame = ttk.Frame(change_destination_window, padding="5 5 15 15")
    dst_frame.grid(column=0, row=0, sticky=(N, W, E, S))

    change_destination_window.columnconfigure(0, weight=1)
    change_destination_window.rowconfigure(0, weight=1)

    ttk.Label(dst_frame, text = "Selected Directory:").grid(row = 1, column  = 1, sticky = W)
    ttk.Label(dst_frame, textvariable = new_label).grid(row = 1, column = 2, sticky = W)

    def prompt_directory():
        destination_directory = files.askdirectory()
        print(destination_directory)
        new_label.set(destination_directory)
        change_destination_window.lift()

    ttk.Button(dst_frame, text = "Browse", command = prompt_directory).grid(row = 1, column = 3, sticky = W)
    
    def confirm_dialogue():
        gui_label.set(new_label.get())
        close_window(change_destination_window)

    ttk.Button(dst_frame, text = "Confirm", command = confirm_dialogue).grid(row = 1, column = 4, sticky = W)

    for child in dst_frame.winfo_children(): child.grid_configure(padx=8, pady=8)
    print("Destination Changed")


def organize(search_prefs, source, destination):

    #print(source.get())
    src_list = os.listdir(source.get())
    src_list_raw = os.listdir(source.get())
    for name in range(len(src_list)):
        src_list[name] = src_list[name][:-4]
    print(src_list)
    tmp_i = 0
    for mov in src_list:
        print(mov)
        tmp_genre = get_genre(mov)
        print(tmp_genre)
        #print(src_list_raw)
        dir_present = detect_directory(destination.get(), str(get_genre(mov)))
        print(dir_present)
        if(dir_present == True):
            shutil.move(str(source.get()+ '\\' + str(src_list_raw[tmp_i])), str(destination.get() + "\\" + get_genre(mov)))
        else:
            os.mkdir(str(destination.get() + "\\" + get_genre(mov)))
            shutil.move(str(source.get()+ '\\' + str(src_list_raw[tmp_i])), str(destination.get() + "\\" + get_genre(mov)))
        tmp_i = tmp_i +1
    
    print("Files Organized")  # probably do this one last


def killProg(program):
    print("Goodbye")
    program.destroy()


def addProfile():
    print("Profile Added")

def view_movie_data():
    movie = 'the matrix'
    print(get_all_data(movie))
    print("wip")

def updateLabels(labels, current):
    print(current)
    for label in range(len(labels)):
        use_label = labels[label]
        use_label.set(config[profiles[current]][config_names[label]+str(current)])

    print('Labels Updated')


def makeGUI():
    root = Tk()  # always first line other than any methods that need to be defined

    root.title("Movie Organizer")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    titlePref = StringVar()  # 0
    releasePref = StringVar()  # 1
    runtimePref = StringVar()  # 2
    directorPref = StringVar()  # 3
    starRatingPref = StringVar()  # 4
    mpaaRatingPref = StringVar()  # 5
    castPref = StringVar()  # 6
    plotPref = StringVar()  # 7
    genrePref = StringVar() # 8

    titlePref.set('true')
    releasePref.set('true')
    runtimePref.set('true')
    directorPref.set('true')
    starRatingPref.set('true')
    mpaaRatingPref.set('true')
    castPref.set('true')
    plotPref.set('true')
    genrePref.set('true')

    sourceFolder = StringVar('')
    destinationFolder = StringVar('')
    fieldPreferences = StringVar('')
    new_source_label = StringVar('')
    new_destination_label = StringVar('')

    new_source_label.set('No new source selected.')

    if defaultStartup == 'DFLT':
        tempString = config[profiles[0]]['destfolder0']
        destinationFolder.set(tempString)
        tempString = config[profiles[0]]['fieldprefs0']
        fieldPreferences.set(tempString)
        tempString = config[profiles[0]]['srcfolder0']
        sourceFolder.set(tempString)
    else:
        indx = profiles.index(defaultStartup)
        tempString = config[profiles[indx]]['DestFolder' + str(indx)]
        destinationFolder.set(tempString)
        tempString = config[profiles[indx]]['FieldPrefs' + str(indx)]
        fieldPreferences.set(tempString)
        tempString = config[profiles[indx]]['SrcFolder' + str(indx)]
        sourceFolder.set(tempString)

    ttk.Label(mainframe, text = "Search Preferences:").grid(column = 1, row = 1, sticky = W)
    ttk.Label(mainframe, textvariable=fieldPreferences).grid(column=2, row=1, sticky=W)  # query preferences
    ttk.Button(mainframe, text="Change",
               command=lambda: changePrefs(root, titlePref, releasePref, runtimePref, directorPref, starRatingPref, mpaaRatingPref, castPref, plotPref, fieldPreferences, genrePref, userProfile.current())).grid(column=4, row=1, sticky=W)  # change prefs

    ttk.Label(mainframe, text = "Source Folder:").grid(column = 1, row = 2, sticky = W)
    ttk.Label(mainframe, textvariable=sourceFolder).grid(column=2, row=2, sticky=W)  # source folder
    ttk.Button(mainframe, text="Change", command= lambda: changeSrc(root, new_source_label, sourceFolder)).grid(column=4, row=2, sticky=W)

    ttk.Label(mainframe, text = "Destination Folder:").grid(column = 1, row = 3, sticky = W)
    ttk.Label(mainframe, textvariable=destinationFolder).grid(column=2, row=3, sticky=W)  # destination Folder
    ttk.Button(mainframe, text="Change", command= lambda: changeDest(root, new_destination_label, destinationFolder)).grid(column=4, row=3, sticky=W)  # change dest

    ttk.Button(mainframe, text="Organize", command=lambda:organize(fieldPreferences, sourceFolder, destinationFolder)).grid(column=1, row=4, sticky=W)  # organize button

    old_labels = [fieldPreferences, sourceFolder, destinationFolder]
    
    userVar = StringVar()
    userProfile = ttk.Combobox(mainframe, textvariable=userVar)
    userProfile.grid(column=3, row=4, sticky=W)
    userProfile['values'] = profiles
    userProfile.current(profiles.index(defaultStartup))
    

    def call_update_labels(x):
        current_profile = userProfile.current()
        updateLabels(old_labels, current_profile)
    
    userProfile.bind('<<ComboboxSelected>>', call_update_labels)

    ttk.Button(mainframe, text = "View Movie Data", command = view_movie_data).grid(row = 4, column = 2, sticky = W)

    ttk.Button(mainframe, text="Add Profile", command=addProfile).grid(column=4, row=4,
                                                                       sticky=W)  # add user profile button
    ttk.Button(mainframe, text="Exit", command=lambda: killProg(root)).grid(column=5, row=4,
                                                                            sticky=W)  # kill program button

    ttk.Button(mainframe, text = "GC", command = lambda: print(gc.collect())).grid(column = 5, row = 1, sticky = W)
    
    for child in mainframe.winfo_children(): child.grid_configure(padx=8, pady=8)

    # root.bind('<Return>', organize)  #bind the enter button to organize.

    root.mainloop()  # always last line

if __name__ == '__main__':
    makeGUI()
