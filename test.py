import threading

from src.interface import Interface
from src.trackball_listener import TrackballListener


def main():
    # create TrackballListener - this will listen for raw displacement data from
    # the trackball computer, process it and then send commands to the interface
    tl = TrackballListener()

    # run the TrackballListener inside its own thread
    tlThread = threading.Thread(target=tl.wait)
    tlThread.start()

    # create + start the interface
    interface = Interface(fullscreen=False)
    interface.start()


if __name__ == "__main__":
    main()
