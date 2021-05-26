from gui import make_gui

from multiprocessing import Process


if __name__ == "__main__":
    gui_process = Process(target=make_gui())
    gui_process.start()