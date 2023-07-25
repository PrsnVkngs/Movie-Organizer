from pathlib import Path
import PySimpleGUI as sG
import configparser
# import pyinstrument

from update_movie_metadata import start_update, folder_update, batch_update
from program_icon import get_icon_base64


# profiler = pyinstrument.Profiler()

# command to compile with nuitka:
# python -m nuitka --disable-console --output-filename='FileFixer' --output-dir='distribution' --enable-plugin=tk-inter --enable-plugin=multiprocessing --follow-imports --standalone '.\IMDB Project\IMDb Query\file_fixer.py'

# command to compile with pyinstaller, just make sure to change the version name.
# pyinstaller -wF '.\IMDB Project\IMDb Query\file_fixer.py' -i 'C:\Users\Crypto Storage\PycharmProjects\Movie-Organizer\filefixericon.ico' -n 'file_fixer_1_3_3.exe'


def create_dir_file(path_str):
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        create_settings_file(path)
    return path


def read_config_file(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config


def run():
    settings_file = create_dir_file(Path.home() / 'Documents/FileFixer/Settings/settings.ini')
    config = read_config_file(settings_file)
    profile = config.get('DEFAULT', 'profile', fallback=None)
    if profile is None:
        create_settings_file(settings_file)
        config = read_config_file(settings_file)
        profile = config.get('DEFAULT', 'profile')

    sG.theme('DarkBlue')

    running = False

    no_movies = 0

    BAR_MAX = 100000
    BAR_INC = 0

    verb = config.getboolean(profile, 'output verbose')
    force = config.getboolean(profile, 'force updates')
    compute = config.getboolean(profile, 'compute stats')

    show_threads = False

    settings_tab = [

        [sG.Text("These logging settings determine the level of detail that is written to the log file.")],
        [sG.Text("Logging Info: 1 = Minimal, 2 = L1+Warnings, 3 = 2+Errors")],
        [sG.Text("Logging level:"), sG.Slider((1, 3), orientation='h', key='-LOGGING_LEVEL-',
                                              default_value=int(config.get(profile, 'logging level'))),
         sG.Checkbox("Output Verbose Mode", key='-VERBOSE-', default=verb)],

        [sG.Text("Force Updates regardless of TMDb Tag:"), sG.Checkbox('Force updates', key='-UPDATE_FORCE-',
                                                                       default=force)],

        [sG.Text("Compute Additional Track Statistics:"), sG.Checkbox('Compute Statistics', key='-STATS-',
                                                                      default=compute)],

        [sG.Text("Log File Location:"), sG.Input(k='-LOG_LOCATION-', visible=True, expand_x=True, expand_y=False,
                                                 default_text=config.get(profile, 'log location')),
         sG.FolderBrowse("Choose Folder", target='-LOG_LOCATION-')],

        [sG.Text("Number of threads:", visible=show_threads),
         sG.Slider((1, 4), orientation='h', key='-THREAD_COUNT-', visible=show_threads,
                   default_value=int(config.get(profile, 'thread count')))]
    ]

    main_tab = [

        [sG.Text('Use the browse button to select individual files. Paste a directory to fix all files within it.')],

        [sG.Input(key='-FILE-', visible=True, expand_x=True, expand_y=False,
                  tooltip="Paste a folder as a directory here:", size=54),
         sG.FilesBrowse("Choose File(s)", target='-FILE-',
                        file_types=(('Matroska Files', '*.mkv'), ('ALL Files', '*.* *'))),
         sG.FolderBrowse("Choose Folder", target='-FILE-'),
         # TODO fix the file selector to handle multiple files.
         sG.Sizer(h_pixels=0, v_pixels=50)
         # sg.Sizer(h_pixels=30, v_pixels=75)
         ],

        [sG.Text("Folder update progress log:")],
        [sG.Multiline(size=(65, 10), expand_x=True, expand_y=True, key='-ACT-', reroute_stdout=True,
                      horizontal_scroll=True, autoscroll=True, reroute_cprint=True)],  # TODO change reroute

        [sG.Text("Folder sorting not started.", key='-PDESC-')],
        [sG.ProgressBar(max_value=BAR_MAX, expand_x=True, expand_y=True, s=(43, 20), p=(5, 10), key='-PROG-')],

        [sG.Button("Run", key='-RUN-'), sG.Button("Clear Log", key='-CLR-'),
         sG.Exit(),
         sG.Sizer(h_pixels=0, v_pixels=40)]

    ]
    # """sG.Button("Cancel", key='-CANCEL-')"""

    layout = [

        [
            sG.TabGroup(
                [
                    [sG.Tab("Main Tab", main_tab),
                     sG.Tab("Settings", settings_tab)]
                ], pad=(3, 10), expand_x=True, expand_y=True
            ),
            sG.Sizegrip(k='-RESIZE-')
        ]

    ]

    window = sG.Window('Movie File Fixer v1.3.4', layout, icon=get_icon_base64(), resizable=True)  # TODO change to True.

    # profiler.start()

    while True:  # The Event Loop
        event, values = window.read()

        match event:
            case sG.WIN_CLOSED | 'Exit':
                try:
                    settings = {
                        'verbose': values.get('-VERBOSE-'),
                        'update-force': values.get('-UPDATE_FORCE-'),
                        'threads': values.get('-THREAD_COUNT-'),
                        'log-location': values.get('-LOG_LOCATION-'),
                        'log-level': values.get('-LOGGING_LEVEL-'),
                        'stats': values.get('-STATS-')
                    }
                    write_settings_file(settings_file, settings)
                except AttributeError:
                    pass
                break

            case '-RUN-':
                # print("Found run case")
                if running:
                    window['-ACT-'].update('There is an action currently running, please wait.', append=True)
                    continue

                path = values.get('-FILE-')
                targets = []
                multi_file = False
                if ';' in path:
                    multi_file = True
                    for paths in str(path).split(';'):
                        targets.append(Path(paths))
                else:
                    targets.append(Path(path))

                # full_path = Path(values.get('-FILE-'))

                if not any(t.exists() for t in targets):
                    sG.cprint("One or more of the files or folders entered does not exist.", colors='white on yellow')

                mkv = targets[0].match("*.mkv")

                running = True
                settings = {
                    'verbose': values.get('-VERBOSE-'),
                    'update-force': values.get('-UPDATE_FORCE-'),
                    'threads': values.get('-THREAD_COUNT-'),
                    'log-location': values.get('-LOG_LOCATION-'),
                    'log-level': values.get('-LOGGING_LEVEL-'),
                    'stats': values.get('-STATS-')
                }

                if multi_file:
                    window.perform_long_operation(lambda: batch_update(targets, window, settings), '-FUPDT-')
                elif mkv:
                    # print("start single update", full_path, "|", full_path.parts)
                    # print("Start single update")
                    window.perform_long_operation(lambda: start_update(targets[0], window, settings), '-SUPDT-')
                else:
                    # print("start folder update", full_path, "|", full_path.parts)
                    # print("Start folder update")
                    window.perform_long_operation(lambda: folder_update(targets[0], window, settings), '-FUPDT-')

            case '-CANCEL-':
                window.write_event_value('-CANCEL-', True)
                print("Cancel event occurred.")

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

            case '-GENERAL_ERROR-':
                error_message_details = values.get('-GENERAL_ERROR-')
                sG.cprint(error_message_details[0], c=error_message_details[1])

            case '-CLR-':
                window['-ACT-'].update('')

    # profiler.stop()
    # profiler.open_in_browser()

    window.close()


def read_settings_file(file_path):
    config = configparser.ConfigParser()

    config.read(file_path)
    return config


def write_settings_file(file_path, values):
    parser = configparser.ConfigParser()
    parser.read(file_path)

    parser['DEFAULT']['logging level'] = str(int(values['log-level']))
    parser['DEFAULT']['output verbose'] = str(values['verbose'])
    parser['DEFAULT']['force updates'] = str(values['update-force'])
    parser['DEFAULT']['thread count'] = str(int(values['threads']))
    parser['DEFAULT']['log location'] = str(values['log-location'])
    parser['DEFAULT']['compute stats'] = str(values['stats'])

    with open(file_path, 'w') as cfg:
        parser.write(cfg)

    return None


def create_settings_file(file_path):
    config = configparser.ConfigParser()

    default_log = Path().home()
    default_log = default_log / 'Documents/FileFixer/Logs'

    config['DEFAULT'] = {
        'Logging Level': 1,
        'Thread Count': 1,
        'Output Verbose': False,
        'Force Updates': False,
        'Compute Stats': False,
        'Log Location': default_log,
        'Profile': 'DEFAULT'
    }

    with file_path.open(mode='w') as cfg:
        config.write(cfg)
        cfg.close()


if __name__ == "__main__":
    run()
