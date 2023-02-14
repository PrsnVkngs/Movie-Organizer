from pathlib import Path
import PySimpleGUI as sG
import configparser

from update_movie_metadata import start_update, folder_update
from program_icon import get_icon_base64


def run():
    settings_file = Path().home()
    settings_file = settings_file / 'Documents/FileFixer/Settings'
    if not settings_file.exists():
        settings_file.mkdir(parents=True, exist_ok=True)

    settings_file = settings_file / 'settings.ini'
    if not settings_file.exists():
        create_settings_file(settings_file)

    config = read_settings_file(settings_file)
    profile = config.get('DEFAULT', 'profile')

    sG.theme('DarkBlue')

    running = False

    no_movies = 0

    BAR_MAX = 100000
    BAR_INC = 0

    settings_tab = [

        [sG.Text("These logging settings determine the level of detail that is written to the log file.")],
        [sG.Text("Logging Info: 1 = Minimal, 2 = L1+Warnings, 3 = 2+Errors")],
        [sG.Text("Logging level:"), sG.Slider((1, 3), orientation='h', key='-LOGGING_LEVEL-',
                                              default_value=int(config.get(profile, 'logging level'))),
         sG.Checkbox("Output Verbose Mode", key='-VERBOSE-', default=bool(config.get(profile, 'output verbose')))],

        [sG.Text("Force Updates regardless of TMDb Tag:"), sG.Checkbox('Force updates', key='-UPDATE_FORCE-',
                                                                       default=bool(config.get(profile, 'force updates')))],

        [sG.Text("Log File Location:"), sG.Input(k='-LOG_LOCATION-', visible=True, expand_x=True, expand_y=False,
                                                 default_text=config.get(profile, 'log location')),
         sG.FolderBrowse("Choose Folder", target='-LOG_LOCATION-')],

        [sG.Text("Number of threads:"), sG.Slider((1, 4), orientation='h', key='-THREAD_COUNT-',
                                                  default_value=int(config.get(profile, 'thread count')))]
    ]

    main_tab = [

        [sG.Text('Use the browse button to select individual files. Paste a directory to fix all files within it.')],

        [sG.Input(key='-FILE-', visible=True, expand_x=True, expand_y=False,
                  tooltip="Paste a folder as a directory here:", size=54),
         sG.FileBrowse("Choose File", target='-FILE-'), sG.FolderBrowse("Choose Folder", target='-FILE-'),
         sG.Sizer(h_pixels=0, v_pixels=50)
         # sg.Sizer(h_pixels=30, v_pixels=75)
         ],

        [sG.Text("Folder update progress log:")],
        [sG.Multiline(size=(65, 10), expand_x=True, expand_y=True, key='-ACT-', reroute_stdout=True,
                      horizontal_scroll=True, autoscroll=True, reroute_cprint=True)],

        [sG.Text("Folder sorting not started.", key='-PDESC-')],
        [sG.ProgressBar(max_value=BAR_MAX, expand_x=True, expand_y=True, s=(43, 20), p=(5, 10), key='-PROG-')],

        [sG.Button("Run", key='-RUN-'), sG.Button("Cancel", key='-CANCEL-'), sG.Button("Clear Log", key='-CLR-'), sG.Exit(),
         sG.Sizer(h_pixels=0, v_pixels=40)]

    ]

    layout = [

        [
            sG.TabGroup(
                [
                    [sG.Tab("Main Tab", main_tab),
                     sG.Tab("Settings", settings_tab)]
                ], pad=(3, 10)
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

                running = True
                window.write_event_value('-CANCEL-', False)
                settings = [values.get('-VERBOSE-'), values.get('-UPDATE_FORCE-'), values.get('-THREAD_COUNT-'),
                            values.get('-LOG_LOCATION-'), values.get('-LOGGING_LEVEL-')]

                if mkv:
                    # print("start single update", full_path, "|", full_path.parts)
                    window.perform_long_operation(lambda: start_update(full_path, window, settings), '-SUPDT-')
                else:
                    # print("start folder update", full_path, "|", full_path.parts)
                    window.perform_long_operation(lambda: folder_update(full_path, window, settings), '-FUPDT-')

            case '-CANCEL-':
                window.write_event_value('-CANCEL-', True)

            case '-SUPDT-' | '-FUPDT-':
                running = False
                print("File fixer has completed running!")

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

            case '-LOGGING_LEVEL-':
                print("Value of LOGGING_LEVEL ", values.get('-LOGGING_LEVEL-'))

            case '-VERBOSE-':
                print("Verbose setting: ", values.get('-VERBOSE-'))

            case '-UPDATE_FORCE-':
                print("Update force state: ", values.get('-UPDATE_FORCE-'))

            case '-LOG_LOCATION-':
                print("Location of the log: ", values.get('-LOG_LOCATION-'))

            case '-THREAD_COUNT-':
                print("Number of threads to use: ", values.get('-THREAD_COUNT-'))

            case '-GENERAL_ERROR-':
                error_message_details = values.get('-GENERAL_ERROR-')
                sG.cprint(error_message_details[0], c=error_message_details[1])

            case '-CLR-':
                window['-ACT-'].update('')

    window.close()


def read_settings_file(file_path):
    config = configparser.ConfigParser()

    config.read(file_path)
    return config


def write_settings_file(file_path):
    return None


def create_settings_file(file_path):
    config = configparser.ConfigParser()

    default_log = Path().home()
    default_log = default_log / 'Documents/FileFixer/Logs'

    config['DEFAULT'] = {
        'Logging Level': 1,
        'Output Verbose': False,
        'Force Updates': False,
        'Log Location': default_log,
        'Thread Count': 1
    }

    with file_path.open(mode='w') as cfg:
        config.write(cfg)
        cfg.close()


if __name__ == "__main__":
    run()
