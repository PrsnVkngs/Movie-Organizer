from pathlib import Path
import PySimpleGUI as sG

from update_movie_metadata import start_update, folder_update
from program_icon import get_icon_base64


def run():
    # program_icon_path = Path('O:/GitHub/Movie-Organizer/IMDB Project/IMDb Query/assets')
    #
    # program_icon = program_icon_path / 'movie_file_editor_icon.ico'

    sG.theme('DarkBlue')

    running = False

    no_movies = 0

    BAR_MAX = 100000
    BAR_INC = 0

    settings_tab = [
        [sG.Text("These logging settings determine the level of detail that is written to the log file.")],
        [sG.Text("Logging Info: 1 = Minimal, 2 = L1+Warnings, 3 = 2+Errors")],
        [sG.Text("Logging level:"), sG.Slider((1, 3), orientation='h', key='-LOGGING_LEVEL-'),
         sG.Checkbox("Output Verbose Mode", key='-VERBOSE-')],
        [sG.Text("Log File Location:"), sG.Input(k='-LOG_LOCATION-', visible=True, expand_x=True, expand_y=False),
         sG.FolderBrowse("Choose Folder", target='-LOG_LOCATION-')],

        [sG.Text("Number of threads:"), sG.Slider((1, 4), 1, orientation='h', key='-THREAD_COUNT-')]
    ]

    main_tab = [

        [sG.Text('Use the browse button to select individual files. Paste a directory to fix all files within it.')],

        [sG.Input(key='-FILE-', visible=True, expand_x=True, expand_y=False,
                  tooltip="Paste a folder as a directory here:", size=54),
         sG.FileBrowse("Choose File", target='-FILE-'), sG.FolderBrowse("Choose Folder", target='-FILE-'),
         sG.Sizer(h_pixels=0, v_pixels=50),
         # sg.Sizer(h_pixels=30, v_pixels=75)
         ],

        [sG.Text("Folder update progress log:")],
        [sG.Multiline(size=(65, 10), expand_x=True, expand_y=True, key='-ACT-', reroute_stdout=True,
                      horizontal_scroll=True, autoscroll=True, reroute_cprint=True)],

        [sG.Text("Folder sorting not started.", key='-PDESC-')],
        [sG.ProgressBar(max_value=BAR_MAX, expand_x=True, expand_y=True, s=(43, 20), p=(5, 10), key='-PROG-')],

        [sG.Button("Run", key='-RUN-'), sG.Button("Clear Log", key='-CLR-'), sG.Exit(), sG.Sizer(h_pixels=0, v_pixels=40)]

    ]

    layout = [

        [
            sG.TabGroup(
                [
                    [sG.Tab("Main Tab", main_tab),
                     sG.Tab("Settings", settings_tab)]
                ], pad=(0, 10)
            ),
            sG.Sizegrip(k='-RESIZE-')
        ]

    ]

    window = sG.Window('Movie File Fixer', layout, icon=get_icon_base64(), resizable=False)  # TODO change to True.

    while True:  # The Event Loop
        event, values = window.read()

        match event:
            case sG.WIN_CLOSED | 'Exit':
                break

            case '-RUN-':
                if running:
                    window['-ACT-'].update('There is an action currently running, please wait.', append=True)
                    continue

                full_path = Path(values.get('-FILE-'))

                if not (full_path.exists()):
                    sG.cprint("Please enter a valid file name or folder.", colors='white on yellow')

                mkv = full_path.match("*.mkv")

                if mkv:
                    # print("start single update", full_path, "|", full_path.parts)
                    running = True
                    window.perform_long_operation(lambda: start_update(full_path, window), '-SUPDT-')
                else:
                    # print("start folder update", full_path, "|", full_path.parts)
                    running = True
                    window.perform_long_operation(lambda: folder_update(full_path, window), '-FUPDT-')

            case '-SUPDT-' | '-FUPDT-':
                running = False

            case '-MOVCOUNT-':
                no_movies = values.get('-MOVCOUNT-')
                window['-PDESC-'].update(f'Progress: 0/{no_movies}')
                try:
                    BAR_INC = BAR_MAX / no_movies
                except ZeroDivisionError:
                    sG.cprint("A folder with no movie files in it has been entered.", colors="black on yellow")

            case '-MOVEPROG-':
                movie_number = values.get('-MOVEPROG-')
                window['-PROG-'].update(movie_number * BAR_INC)
                window['-PDESC-'].update(f'Progress: {movie_number}/{no_movies}')

            case '-TMDBERR-':
                sG.cprint(
                    f"There was an issue getting TMDB Data for the movie {values.get('-TMDBERR-')}. Metadata will "
                    f"still be fixed, however, title tag will not.", c='white on red')

            case '-GENERAL_ERROR-':
                error_message_details = values.get('-GENERAL_ERROR-')
                sG.cprint(error_message_details[0], c=error_message_details[1])

            case '-CLR-':
                window['-ACT-'].update('')

    window.close()


if __name__ == "__main__":
    run()
