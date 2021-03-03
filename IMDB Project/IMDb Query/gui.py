# remember to remove make_gui call at the bottom when done
# GUI code for movie organizer project
# Due for heavy rewriting using more python concepts and code cleanup.

# python libraries
import configparser
from tkinter import *
from tkinter import filedialog as files
from tkinter import ttk

# my libraries
from move_files import *

# title, release date, runtime, director, starrating, mpaarating, cast, plot, genre
noFields = 7
prefs = ['true'] * noFields
prefName = ['Title', 'Release date', 'Runtime', 'Director', 'Star Rating', 'MPAA Rating', 'Genre']

config_names = ['fieldprefs', 'srcfolder', 'destfolder']

config = configparser.ConfigParser()
config.read('user_preferences.ini')

source_directory = ''
destination_directory = ''

acceptable_rating = float(0)


def get_profiles(cfg):
    return cfg.sections()


profiles = get_profiles(config)
defaultStartup = config[profiles[0]]['defaultprofile']
defaultStartup = str(defaultStartup)
number_of_profiles = config[profiles[0]]['numberprofiles']
profiles = profiles[1:]


# might remove this function, not 100% why it was made or its current use.
def get_movie_data(data, movie):
    # tmp_data =
    print('wip')


# also unsure about the use of this function, might delete as well.
def view_movie_data():
    movie = 'the matrix'
    print(get_all_data(movie))
    print("wip")


# end file management functions

def kill_prog(program):
    print("Goodbye")
    program.destroy()


def close_window(window):
    window.destroy()
    gc.collect()


def change_prefs(parent, title_pref, release_pref, runtime_pref, director_pref, star_rating_pref, mpaa_rating_pref,
                 field_prefs,
                 genre_pref, selected_profile):
    prefs_window = Toplevel(parent)
    prefs_window.title("Select new search preferences")
    pref_frame = ttk.Frame(prefs_window, padding="5 5 15 15")
    pref_frame.grid(column=0, row=0, sticky=(N, W, E, S))

    prefs_window.columnconfigure(0, weight=1)
    prefs_window.rowconfigure(0, weight=1)

    ttk.Checkbutton(pref_frame, text='Title', command=lambda: update_prefs(0, title_pref.get()), variable=title_pref,
                    onvalue='true', offvalue='false').grid(column=1, row=1, sticky=W)
    ttk.Checkbutton(pref_frame, text='Release Year', command=lambda: update_prefs(1, release_pref.get()),
                    variable=release_pref, onvalue='true', offvalue='false').grid(column=2, row=1, sticky=W)
    ttk.Checkbutton(pref_frame, text='Runtime', command=lambda: update_prefs(2, runtime_pref.get()),
                    variable=runtime_pref,
                    onvalue='true', offvalue='false').grid(column=3, row=1, sticky=W)
    ttk.Checkbutton(pref_frame, text='Director', command=lambda: update_prefs(3, director_pref.get()),
                    variable=director_pref, onvalue='true', offvalue='false').grid(column=1, row=2, sticky=W)
    ttk.Checkbutton(pref_frame, text='Star Rating', command=lambda: update_prefs(4, star_rating_pref.get()),
                    variable=star_rating_pref, onvalue='true', offvalue='false').grid(column=2, row=2, sticky=W)
    ttk.Checkbutton(pref_frame, text='MPAA Rating', command=lambda: update_prefs(5, mpaa_rating_pref.get()),
                    variable=mpaa_rating_pref, onvalue='true', offvalue='false').grid(column=3, row=2, sticky=W)
    # ttk.Checkbutton(pref_frame, text='Cast', command=lambda: update_prefs(6, castPref.get()), variable=castPref,
    #                onvalue='true', offvalue='false').grid(column=1, row=3, sticky=W)
    # ttk.Checkbutton(pref_frame, text='Plot', command=lambda: update_prefs(7, plotPref.get()), variable=plotPref,
    #               onvalue='true', offvalue='false').grid(column=2, row=3, sticky=W)
    ttk.Checkbutton(pref_frame, text='Genre', command=lambda: update_prefs(6, genre_pref.get()), variable=genre_pref,
                    onvalue='true', offvalue='false').grid(column=2, row=3, sticky=W)

    ttk.Button(pref_frame, text='Confirm',
               command=lambda: push_field_INI(field_prefs, selected_profile, prefs_window)).grid(column=1, row=4,
                                                                                                 sticky=W)
    ttk.Button(pref_frame, text='Close Window', command=lambda: close_window(prefs_window)).grid(column=3, row=4,
                                                                                                 sticky=W)
    # lf = ttk.Labelframe(prefs_window, text = "Select the data you would like to be retrieved")

    for child in pref_frame.winfo_children(): child.grid_configure(padx=8, pady=8)

    print("Preferences Changed")


# this code will get the selected preferences from the GUI, then push them to the preferences file.
def push_field_INI(fields, slctd_prof, window):
    preferences = ''
    for boo in range(noFields):
        if prefs[boo] == 'true':
            temp = ' ' + prefName[boo] + ','
            preferences += temp
    preferences = preferences[0:len(preferences) - 1]

    fields.set(preferences)

    if slctd_prof == 0:
        print('Add a new profile or select a different one to push to ini, as Default is selected.')
    else:
        currentProf = profiles[slctd_prof]
        # config[str(currentProf)][str('destFolder'+str(slctdProf))]
        config[str(currentProf)][str('fieldPrefs' + str(slctd_prof))] = str(preferences)
        print(str(preferences))

    with open('user_preferences.ini', 'w') as writeconfig:
        config.write(writeconfig)
    writeconfig.close()

    close_window(window)

    print('INI File Updated')


def update_prefs(pref_no, value):
    prefs[pref_no] = value


def push_src_INI(src):
    new_src = src


def push_dst_INI(dst):
    new_dst = dst


# this method will bring up a new window that allows the user to specify a new
# directory for the program to get files from
def change_src(parent, new_label, gui_label):
    change_source_window = Toplevel(parent)
    change_source_window.title("Select new source directory")
    src_frame = ttk.Frame(change_source_window, padding="5 5 15 15")
    src_frame.grid(column=0, row=0, sticky=(N, W, E, S))

    change_source_window.columnconfigure(0, weight=1)
    change_source_window.rowconfigure(0, weight=1)

    ttk.Label(src_frame, text="Selected Directory:").grid(row=1, column=1, sticky=W)
    directiontext = ttk.Label(src_frame, textvariable=new_label).grid(row=1, column=2, sticky=W)

    def prompt_directory():
        source_directory = files.askdirectory()
        print(source_directory)
        new_label.set(source_directory)
        change_source_window.lift()

    change_src_button = ttk.Button(src_frame, text="Browse", command=prompt_directory).grid(row=1, column=3, sticky=W)

    def confirm_dialogue():
        gui_label.set(new_label.get())
        close_window(change_source_window)

    confirm_button = ttk.Button(src_frame, text="Confirm", command=confirm_dialogue).grid(row=1, column=4, sticky=W)

    for child in src_frame.winfo_children(): child.grid_configure(padx=8, pady=8)

    print("Source Changed")


# This funciton will open a new window that will allow the user to
# specify a new destination folder for the program to sort movies.
def change_dest(parent, new_label, gui_label):
    change_destination_window = Toplevel(parent)
    change_destination_window.title("Select new destination folder")
    dst_frame = ttk.Frame(change_destination_window, padding="5 5 15 15")
    dst_frame.grid(column=0, row=0, sticky=(N, W, E, S))

    change_destination_window.columnconfigure(0, weight=1)
    change_destination_window.rowconfigure(0, weight=1)

    ttk.Label(dst_frame, text="Selected Directory:").grid(row=1, column=1, sticky=W)
    ttk.Label(dst_frame, textvariable=new_label).grid(row=1, column=2, sticky=W)

    def prompt_directory():
        destination_directory = files.askdirectory()
        print(destination_directory)
        new_label.set(destination_directory)
        change_destination_window.lift()

    ttk.Button(dst_frame, text="Browse", command=prompt_directory).grid(row=1, column=3, sticky=W)

    def confirm_dialogue():
        gui_label.set(new_label.get())
        close_window(change_destination_window)

    ttk.Button(dst_frame, text="Confirm", command=confirm_dialogue).grid(row=1, column=4, sticky=W)

    for child in dst_frame.winfo_children(): child.grid_configure(padx=8, pady=8)
    print("Destination Changed")


# this function organizes movies based on genre using the source files provided by the user
# then sorts and moves them to the given destination folder.
def organize(search_prefs, source, destination, rt):
    src_str = source.get()
    dst_str = destination.get()

    acc_rating = float(rt.get())

    walk_directory(src_str, dst_str, acc_rating)

    # print(type(src_str))
    # print(type(source.get()))
    # src_list = os.listdir(src_str)
    # src_list_raw = os.listdir(src_str)

    # use os.walk to traverse the file system, use a movies and folder variable and append a list to them at the very beginning of the loop.
    # use a level_count integer variable to count the levels, then append the folders and movies on each level.
    # then, add one to the level_count and restart the loop.

    # this will trim the file extension from the files in the source
    # need to make it more intelligent as it doesn't consider whether it is -
    # a file or a folder.

    # for name in range(len(src_list)):
    # src_list[name] = src_list[name][:-4]
    #    for movie in src_list:
    #        movie = movie[:-4]

    # print(src_list)
    # tmp_i = 0
    # for mov in src_list:
    # print(mov)
    # tmp_genre = get_genre(mov)
    # print(tmp_genre)
    # print(src_list_raw)
    # dir_present = detect_directory(dst_str, tmp_genre) #variable determines whether the directory for the genre is present or not. true if yes, false if no.
    # print(dir_present)

    # tmp_i = tmp_i +1

    print("Files Organized")  # probably do this one last


# This function will take the values stored in the labels for search preferences,
# source directory, and destination directory, and write them to the ini file with
# a user specified name.
def add_profile(parent, source, dest):
    new_prof = Toplevel(parent)
    new_prof.title("Add new Organize Profile")
    prof_frame = ttk.Frame(new_prof, padding="3 3 12 12")
    prof_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    new_prof.columnconfigure(0, weight=1)
    new_prof.rowconfigure(0, weight=1)

    ttk.Label(prof_frame,
              text="When adding a new profile, make sure you set preferences to what you want them to be first.").grid(
        column=1, row=1)
    ttk.Label(prof_frame, text="Write the new profile name here:").grid(column=1, row=2)

    prof_var = StringVar('')
    prof_name = ttk.Entry(prof_frame, textvariable=prof_var).grid(column=2, row=2)

    def add_profile():
        global number_of_profiles  # instantiate reference to global number_of_profiles variable
        source_value = source.get()
        destination_value = dest.get()
        prefs_value = ''
        for boo in range(noFields):
            if prefs[boo] == 'true':
                temp = ' ' + prefName[boo] + ','
                prefs_value += temp
        prefs_value = prefs_value[0:len(prefs_value) - 1]

        # make variables for the string labeling the values.
        new_section_name = prof_var.get().upper()
        nopro = str(number_of_profiles)  # variable for number of profiles
        pref_string = 'fieldprefs' + nopro
        src_string = 'srcfolder' + nopro
        dst_string = 'destfolder' + nopro

        # add sections to the ini file loaded in the program memory
        config.add_section(new_section_name)
        config.set(new_section_name, pref_string, prefs_value)
        config.set(new_section_name, src_string, source_value)
        config.set(new_section_name, dst_string, destination_value)

        number_of_profiles = str(int(number_of_profiles) + 1)
        config.set('STARTUP', 'numberprofiles', str(number_of_profiles))  # add one to number of profiles

        # open config ini file and write new values to hard file
        with open('user_preferences.ini', 'w') as configfile:
            config.write(configfile)
        configfile.close()  # close the configfile

        close_window(new_prof)  # close the popup window

    ttk.Button(prof_frame, text="Confirm", command=add_profile).grid(column=1, row=3)

    print("Profile Added")


def update_labels(labels, current, star_entry):
    print(current)
    for label in range(len(labels)):
        use_label = labels[label]
        use_label.set(config[profiles[current]][config_names[label] + str(current)])
    star_entry.set(config[profiles[current]]['lowestrating' + str(current)])
    print('Labels Updated')


def make_gui():
    root = Tk()  # always first line other than any methods that need to be defined

    root.title("Movie Organizer")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    title_pref = StringVar()  # 0
    release_pref = StringVar()  # 1
    runtime_pref = StringVar()  # 2
    director_pref = StringVar()  # 3
    star_rating_pref = StringVar()  # 4
    mpaa_rating_pref = StringVar()  # 5
    # castPref = StringVar()  # 6
    # plotPref = StringVar()  # 7
    genre_pref = StringVar()  # 8

    lowest_acceptable_rating = StringVar('')

    title_pref.set('true')
    release_pref.set('true')
    runtime_pref.set('true')
    director_pref.set('true')
    star_rating_pref.set('true')
    mpaa_rating_pref.set('true')
    # castPref.set('true')
    # plotPref.set('true')
    genre_pref.set('true')

    source_folder = StringVar('')
    destination_folder = StringVar('')
    field_preferences = StringVar('')
    new_source_label = StringVar('')
    new_destination_label = StringVar('')

    new_source_label.set('No new source selected.')

    if defaultStartup == 'DFLT':
        temp_string = config[profiles[0]]['destfolder0']
        destination_folder.set(temp_string)
        temp_string = config[profiles[0]]['fieldprefs0']
        field_preferences.set(temp_string)
        temp_string = config[profiles[0]]['srcfolder0']
        source_folder.set(temp_string)
        temp_string = config[profiles[0]]['lowestrating0']
        lowest_acceptable_rating.set(temp_string)
    else:
        indx = profiles.index(defaultStartup)
        temp_string = config[profiles[indx]]['DestFolder' + str(indx)]
        destination_folder.set(temp_string)
        temp_string = config[profiles[indx]]['FieldPrefs' + str(indx)]
        field_preferences.set(temp_string)
        temp_string = config[profiles[indx]]['SrcFolder' + str(indx)]
        source_folder.set(temp_string)
        temp_string = config[profiles[indx]]['lowestrating' + str(indx)]
        lowest_acceptable_rating.set(temp_string)

    ttk.Label(mainframe, text="Search Preferences:").grid(column=1, row=1, sticky=W)
    ttk.Label(mainframe, textvariable=field_preferences).grid(column=2, row=1, sticky=W)  # query preferences
    ttk.Button(mainframe, text="Change",
               command=lambda: change_prefs(root, title_pref, release_pref, runtime_pref, director_pref, star_rating_pref,
                                            mpaa_rating_pref, field_preferences, genre_pref, user_profile.current())).grid(
        column=4, row=1, sticky=W)  # change prefs

    ttk.Label(mainframe, text="Source Folder:").grid(column=1, row=2, sticky=W)
    ttk.Label(mainframe, textvariable=source_folder).grid(column=2, row=2, sticky=W)  # source folder
    ttk.Button(mainframe, text="Change", command=lambda: change_src(root, new_source_label, source_folder)).grid(column=4,
                                                                                                                row=2,
                                                                                                                sticky=W)

    ttk.Label(mainframe, text="Destination Folder:").grid(column=1, row=3, sticky=W)
    ttk.Label(mainframe, textvariable=destination_folder).grid(column=2, row=3, sticky=W)  # destination Folder
    ttk.Button(mainframe, text="Change",
               command=lambda: change_dest(root, new_destination_label, destination_folder)).grid(column=4, row=3,
                                                                                                 sticky=W)  # change dest

    ttk.Button(mainframe, text="Organize Files",
               command=lambda: organize(field_preferences, source_folder, destination_folder,
                                        lowest_acceptable_rating)).grid(column=1, row=4, sticky=W)  # organize button

    old_labels = [field_preferences, source_folder, destination_folder]

    user_var = StringVar()
    user_profile = ttk.Combobox(mainframe, textvariable=user_var)
    user_profile.grid(column=3, row=4, sticky=W)
    user_profile['values'] = profiles
    user_profile.current(profiles.index(defaultStartup))

    # this Entry box belongs lower in the code but i have to put it here due to pyton bs.
    # i'm probably not doing it the right way but i'm not experienced enough in python yet.

    def call_update_labels(x):
        current_profile = user_profile.current()
        update_labels(old_labels, current_profile, lowest_acceptable_rating)

    user_profile.bind('<<ComboboxSelected>>', call_update_labels)

    # ttk.Button(mainframe, text = "View Movie Data", command = view_movie_data).grid(row = 4, column = 2, sticky = W)

    ttk.Label(mainframe, text="Organization Profile:").grid(column=2, row=4, sticky=E)

    ttk.Button(mainframe, text="Add Profile",
               command=lambda: add_profile(root, new_source_label, new_destination_label)).grid(column=4, row=4,
                                                                                                sticky=W)  # add user profile button
    ttk.Button(mainframe, text="Exit", command=lambda: kill_prog(root)).grid(column=5, row=4,
                                                                             sticky=W)  # kill program button

    ttk.Button(mainframe, text="GC", command=lambda: print(gc.collect())).grid(column=5, row=1, sticky=W)

    star_entry = ttk.Entry(mainframe, textvariable=lowest_acceptable_rating).grid(column=2, row=5)
    ttk.Label(mainframe, text="Enter the lowest acceptable star rating for a movie:").grid(row=5, column=1)

    for child in mainframe.winfo_children(): child.grid_configure(padx=8, pady=8)

    # root.bind('<Return>', organize)  #bind the enter button to organize.

    root.mainloop()  # always last line


if __name__ == '__main__':
    make_gui()
