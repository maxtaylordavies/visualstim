from typing import Any, Dict, Optional

from psychopy.visual import Window

from src.components import SyncSquares
from src.constants import (
    DEFAULT_PARAMS,
    SYNC_PULSE_LENGTH,
    DEFAULT_BACKGROUND_COLOR,
    STIMULATION_BACKGROUND_COLOR,
)
from src.utils import checkForEsc


class Stimulus:
    def __init__(self) -> None:
        self.duration = 0

    def drawFrame(self) -> None:
        pass


def playStimulus(
    window: Window,
    stimulus: Stimulus,
    frameRate: float,
    syncSquares: Optional[SyncSquares],
    params: Dict[str, Any] = DEFAULT_PARAMS,
    callback: Any = None,
    shouldTerminate: Any = checkForEsc,
):
    window.color = STIMULATION_BACKGROUND_COLOR

    # 2P (+ maybe camera) trigger loop
    if syncSquares:
        syncSquares.toggle(1)  # turn on trigger square
        for i in range(int(frameRate * params["sync"]["trigger duration"])):
            # check if we should terminate
            if shouldTerminate():
                break

            # execute per-frame callback
            if callback:
                callback()

            if i == 3:
                syncSquares.toggle(1)  # turn off trigger square

            syncSquares.draw()
            window.flip()

    # main display loop
    duration = params["stimulus"]["stimulus duration"] or stimulus.duration
    print(duration)
    for frameIdx in range(int(frameRate * duration)):
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

        # draw stimulus (+ sync squares)
        stimulus.drawFrame()
        if syncSquares:
            syncSquares.draw()
        window.flip()

    # turn off sync square
    if syncSquares:
        syncSquares.turn_off(0)

    window.color = DEFAULT_BACKGROUND_COLOR
    window.flip()