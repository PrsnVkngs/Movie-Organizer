import PySimpleGUI as sg
# from multiprocessing import Process

from update_movie_metadata import start_update, folder_update


# folder_thread = Process()


def run():
    sg.theme('DarkBlue')

    # original_dir = os.getcwd()

    # BAR_MAX = 100

    layout = [

        [sg.Text('Use the browse button to select individual files. Paste a directory to fix all files within it.')],

        [sg.Input(key='-FILE-', visible=True), sg.FileBrowse(),
         sg.Sizer(h_pixels=30, v_pixels=50),
         sg.Sizer(h_pixels=30, v_pixels=75)],

        # [sg.Text("Program not started: Start to get a progress bar.")],
        # [sg.ProgressBar(BAR_MAX, orientation='h', size=(40, 15), key='-PROG-')],
        # sg.Sizer(h_pixels=0, v_pixels=75),
        [sg.Button("Run", key='-RUN-'), sg.Exit()]

    ]

    window = sg.Window('Movie File Fixer', layout)

    while True:  # The Event Loop
        event, values = window.read()
        # print(event, "|\t|", values)
        if event == '-RUN-':
            full_path = values.get('-FILE-').replace('/', '\\').strip()

            # print(full_path[-3:])
            if full_path[-3:] == 'mkv':
                mkv = True
                right_split = full_path.rsplit('\\', 1)
                movie = right_split[1]
                path = right_split[0]
            else:
                mkv = False
                path = full_path

            if mkv:
                # print("start single update", full_path, "|",  path, "|",  movie)
                start_update(path, movie)
            else:
                # print("start folder update", full_path, "doesn't work")
                folder_update(full_path)

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

    window.close()


if __name__ == "__main__":
    run()
