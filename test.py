from src.interface import Interface


def main():
    interface = Interface(fullscreen=True)
    # interface.loadExperiment("test.json")
    interface.start()


if __name__ == "__main__":
    main()
