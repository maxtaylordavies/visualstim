import numpy as np
from psychopy import visual, core

from grating import grating
from textures import drumTexture
from components import Button, PlayButton
from interface import Interface


def onStartClicked(interface):
    texture = drumTexture(interface.frameRate)
    grating(interface.window, texture, 10, interface.frameRate)


def main():
    # create window
    # win = visual.Window(fullscr=False, units="norm", color=[0, 0, 0])
    # frameRate = win.getActualFrameRate()

    # b = button("Test button")
    # b.draw()
    # win.flip()

    # # get texture for drum grating
    # texture = drumTexture(frameRate)

    # # run grating
    # grating(win, texture, 60, frameRate)
    interface = Interface(components=[PlayButton(40, [350, -250], onStartClicked)])
    interface.run()


if __name__ == "__main__":
    main()
