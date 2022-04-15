from typing import List

from psychopy.visual import Window, GratingStim

from utils import checkForEsc
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, GREY, BLACK, WHITE
from components import SyncSquares


def grating(
    window: Window, syncSquares: SyncSquares, texture, duration: List[int], frameRate
):
    triggerDuration, stimDuration = duration

    # initialise grating object
    grating = GratingStim(win=window, size=[WINDOW_HEIGHT, WINDOW_WIDTH], units="pix")

    # camera trigger loop
    syncSquares.toggle(1)  # turn on bottom sync square
    for i in range(int(frameRate * triggerDuration)):
        # exit if user presses esc
        if checkForEsc():
            break

        if i == 3:
            syncSquares.toggle(1)  # turn off bottom sync square

        window.color = GREY
        syncSquares.draw()
        window.flip()

    window.color = WHITE

    # main display loop
    syncSquares.toggle(0)  # turn on top sync square
    frameIdx = 0
    for _ in range(int(frameRate * stimDuration)):
        # exit if user presses esc
        if checkForEsc():
            break

        # update grating texture
        grating.tex = texture[frameIdx]

        # draw the new frame
        grating.draw()
        syncSquares.draw()
        window.flip()

        # increment the frame counter
        frameIdx = (frameIdx + 1) % len(texture)

    # turn off top sync square
    syncSquares.toggle(0)
