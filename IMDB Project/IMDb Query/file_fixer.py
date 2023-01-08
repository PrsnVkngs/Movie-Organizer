import PySimpleGUI as sg
import threading


from update_movie_metadata import start_update, folder_update


# folder_thread = Process()


def run():
    sg.theme('DarkBlue')

    running = False

    no_movies = 0

    BAR_MAX = 100000
    BAR_INC = 0

    layout = [

        [sg.Text('Use the browse button to select individual files. Paste a directory to fix all files within it.')],

        [sg.Input(key='-FILE-', visible=True, tooltip="Paste a folder as a directory here:", size=54),
         sg.FileBrowse("Choose File"),
         sg.Sizer(h_pixels=30, v_pixels=50),
         sg.Sizer(h_pixels=30, v_pixels=75)],

        [sg.Text("Folder update progress log:")],
        [sg.Multiline(size=(65, 10), key='-ACT-', reroute_stdout=True, horizontal_scroll=True, autoscroll=True,
                      reroute_cprint=True)],

        [sg.Text("Folder sorting not started.", key='-PDESC-')],
        [sg.ProgressBar(max_value=BAR_MAX, s=(43, 20), p=(5, 10), key='-PROG-')],

        [sg.Button("Run", key='-RUN-'), sg.Button("Clear Log", key='-CLR-'), sg.Exit()]

    ]

    window = sg.Window('Movie File Fixer', layout)

    while True:  # The Event Loop
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
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

            if mkv and not running:
                # print("start single update", full_path, "|",  path, "|",  movie)
                running = True
                window.perform_long_operation(lambda: start_update(path, movie, window), '-SUPDT-')
            elif not running:
                # print("start folder update", full_path, "doesn't work")
                running = True
                window.perform_long_operation(lambda: folder_update(full_path, window), '-FUPDT-')
            else:
                window['-ACT-'].update('There is an action currently running, please wait.', append=True)

        if event == '-SUPDT-' or '-FUPDT-':
            running = False

        if event == '-MOVCOUNT-':
            no_movies = values.get('-MOVCOUNT-')
            window['-PDESC-'].update(f'Progress: 0/{no_movies}')
            BAR_INC = BAR_MAX / no_movies

        if event == '-MOVEPROG-':
            movie_number = values.get('-MOVEPROG-')
            window['-PROG-'].update(movie_number * BAR_INC)
            window['-PDESC-'].update(f'Progress: {movie_number}/{no_movies}')

        if event == '-TMDBERR-':
            sg.cprint(f"There was an issue getting TMDB Data for the movie {values.get('-TMDBERR-')}. Metadata will "
                      f"still be fixed, however, title tag will not.", c='white on red')

        if event == '-CLR-':
            window['-ACT-'].update('')

    window.close()


if __name__ == "__main__":
    run()
