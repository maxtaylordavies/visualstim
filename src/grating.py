from typing import Any, Dict, List, Optional

from psychopy.visual import Window, GratingStim
from psychopy.event import Mouse

from src.utils import checkForEsc, noOp
from src.constants import WINDOW_WIDTH, GREY, WHITE, DEFAULT_PARAMS, SYNC_PULSE_LENGTH
from src.components import SyncSquares


def grating(
    window: Window,
    syncSquares: Optional[SyncSquares],
    texture: List,
    frameRate: float,
    params: Dict[str, Any] = DEFAULT_PARAMS,
    callback: Any = None,
    shouldTerminate: Any = checkForEsc,
) -> None:
    # initialise grating object
    grating = GratingStim(
        win=window,
        size=[WINDOW_WIDTH, WINDOW_WIDTH],
        units="pix",
        ori=params["stimulus"]["orientation"],
    )

    # 2P (+ maybe camera) trigger loop
    if syncSquares:
        syncSquares.toggle(1)  # turn on trigger square
        for i in range(int(frameRate * params["sync"]["trigger duration"])):
            # check if we should terminate
            if shouldTerminate():
                break

            # # exit if user presses esc
            # if checkForEsc():
            #     break

            # execute per-frame callback
            if callback:
                callback()

            if i == 3:
                syncSquares.toggle(1)  # turn off trigger square

            window.color = GREY
            syncSquares.draw()
            window.flip()

        window.color = WHITE

    # main display loop
    frameIdx = 0
    for _ in range(int(frameRate * params["stimulus"]["stimulus duration"])):
        # check if we should terminate
        if shouldTerminate():
            break

        # exit if user presses esc
        # if checkForEsc():
        #     break

        # execute per-frame callback
        if callback:
            callback()

        # send a sync pulse if needed
        if syncSquares and frameIdx % params["sync"]["sync interval"] in {
            0,
            SYNC_PULSE_LENGTH,
        }:
            syncSquares.toggle(0)

        # update grating texture
        grating.tex = texture[frameIdx % len(texture)]

        # draw the new frame
        grating.draw()
        if syncSquares:
            syncSquares.draw()
        window.flip()

        # increment the frame counter
        frameIdx += 1

    # turn off sync square
    if syncSquares:
        syncSquares.turn_off(0)
