from typing import Any, Dict, List, Optional

from psychopy.visual import Window
from psychopy.visual.movie3 import MovieStim3

from src.components import SyncSquares
from src.utils import checkForEsc
from src.constants import WINDOW_WIDTH, GREY, WHITE, DEFAULT_PARAMS, SYNC_PULSE_LENGTH


def movie(
    window: Window,
    path: str,
    syncSquares: Optional[SyncSquares],
    frameRate: float,
    params: Dict[str, Any] = DEFAULT_PARAMS,
    callback: Any = None,
    shouldTerminate: Any = checkForEsc,
) -> None:
    # read file from given path + initialise movie object
    _movie = MovieStim3(window, path, volume=0.0)

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
    for frameIdx in range(int(frameRate * _movie.duration)):
        # check if we should terminate
        if shouldTerminate():
            break

        # execute per-frame callback
        if callback:
            callback()

        # send a sync pulse if needed
        if syncSquares and frameIdx % params["sync"]["sync interval"] in {
            0,
            SYNC_PULSE_LENGTH,
        }:
            syncSquares.toggle(0)

        # draw the next frame of the movie
        _movie.draw()
        window.flip()

    # turn off sync square
    if syncSquares:
        syncSquares.turn_off(0)
