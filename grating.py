from psychopy import visual

from utils import checkForEsc
from constants import WINDOW_WIDTH, WINDOW_HEIGHT


def grating(window, texture, duration, frameRate):
    # initialise grating object
    grating = visual.GratingStim(
        win=window, size=[WINDOW_HEIGHT, WINDOW_WIDTH], units="pix"
    )

    # main display loop
    frameIdx = 0
    for _ in range(int(frameRate * duration)):
        # exit if user presses esc
        if checkForEsc():
            return

        # update grating texture
        grating.tex = texture[frameIdx]

        # draw the new frame
        grating.draw()
        window.flip()

        # increment the frame counter
        frameIdx = (frameIdx + 1) % len(texture)
