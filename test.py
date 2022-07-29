from argparse import ArgumentParser
import threading
import sys

from src.interface import Interface
from src.trackball_listener import TrackballListener


def main():
    print(sys.argv)

    parser = ArgumentParser()
    parser.add_argument("--trackball", action="store_true")
    parser.add_argument("--no-trackball", dest="trackball", action="store_false")
    parser.set_defaults(trackball=True)

    args = parser.parse_args()

    if args.trackball:
        # create TrackballListener - this will listen for raw displacement data from
        # the trackball computer, process it and then send commands to the interface
        tl = TrackballListener()

        # run the TrackballListener inside its own thread
        tlThread = threading.Thread(target=tl.wait)
        tlThread.start()

    # create + start the interface
    interface = Interface(fullscreen=False, listenUDP=args.trackball)
    interface.start()


if __name__ == "__main__":
    main()
