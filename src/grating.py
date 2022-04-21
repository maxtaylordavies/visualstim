from typing import Any, Dict, List
from psychopy.visual import Window, GratingStim

from src.utils import checkForEsc
from src.constants import WINDOW_WIDTH, GREY, WHITE, DEFAULT_PARAMS
from src.components import SyncSquares


def grating(
    window: Window,
    syncSquares: SyncSquares,
    texture: List,
    frameRate: float,
    params: Dict[str, Any] = DEFAULT_PARAMS,
) -> None:
    # initialise grating object
    grating = GratingStim(
        win=window,
        size=[WINDOW_WIDTH, WINDOW_WIDTH],
        units="pix",
        ori=params["stimulus"]["orientation"],
    )

    # camera trigger loop
    syncSquares.toggle(1)  # turn on bottom sync square
    for i in range(int(frameRate * params["sync"]["trigger duration"])):
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
    for _ in range(int(frameRate * params["stimulus"]["stimulus duration"])):
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
