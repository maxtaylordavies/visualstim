from typing import Any, Dict, List
from psychopy.visual import Window, GratingStim

from src.utils import checkForEsc
from src.constants import WINDOW_WIDTH, GREY, WHITE, DEFAULT_PARAMS, SYNC_PULSE_LENGTH
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

    # 2P trigger loop
    syncSquares.toggle(1)  # turn on trigger square
    for i in range(int(frameRate * params["sync"]["trigger duration"])):
        # exit if user presses esc
        if checkForEsc():
            break

        if i == 3:
            syncSquares.toggle(1)  # turn off trigger square

        window.color = GREY
        syncSquares.draw()
        window.flip()

    window.color = WHITE

    # main display loop
    frameIdx = 0
    for _ in range(int(frameRate * params["stimulus"]["stimulus duration"])):
        # exit if user presses esc
        if checkForEsc():
            break

        # send a sync pulse if needed
        if frameIdx % params["sync"]["sync interval"] in {0, SYNC_PULSE_LENGTH}:
            syncSquares.toggle(0)

        # update grating texture
        grating.tex = texture[frameIdx % len(texture)]

        # draw the new frame
        grating.draw()
        syncSquares.draw()
        window.flip()

        # increment the frame counter
        frameIdx += 1

    # turn off sync square
    syncSquares.turn_off(0)
