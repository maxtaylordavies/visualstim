from typing import Any, Dict, List, Optional

from psychopy.visual import Window

from src.components import SyncSquares
from src.constants import (
    DEFAULT_PARAMS,
    DEFAULT_BACKGROUND_COLOR,
    STIMULATION_BACKGROUND_COLOR,
)
from src.utils import checkForEsc


class Stimulus:
    def __init__(
        self, window: Window, frameRate: float, params: Dict[str, Any] = DEFAULT_PARAMS
    ) -> None:
        self.window = window
        self.frameRate = frameRate
        self.params = params
        self.duration = 0
        self.frameIdx = 0

    def drawFrame(self) -> None:
        pass


def playStimuli(
    window: Window,
    stimuli: List[Stimulus],
    frameRate: float,
    syncSquares: Optional[SyncSquares],
    paramsList: List[Dict[str, Any]] = [],
    callback: Any = None,
    shouldTerminate: Any = checkForEsc,
):
    window.color = STIMULATION_BACKGROUND_COLOR
    params = paramsList[0] if paramsList else DEFAULT_PARAMS

    # trigger loop
    if syncSquares:
        syncSquares.toggle(1)  # turn on trigger square
        for i in range(int(frameRate * params["sync"]["trigger duration"])):
            # check if we should terminate
            if shouldTerminate():
                break

            # execute per-frame callback
            if callback:
                callback()

            if i == params["sync"]["pulse length"]:
                syncSquares.toggle(1)  # turn off trigger square

            syncSquares.draw()
            window.flip()

    # cycle through + display stimuli
    for i in range(len(stimuli)):
        p = paramsList[i] if i < len(paramsList) else DEFAULT_PARAMS
        playStimulus(
            window, stimuli[i], frameRate, syncSquares, p, callback, shouldTerminate
        )

    # reset window colour
    window.color = DEFAULT_BACKGROUND_COLOR
    window.flip()


def playStimulus(
    window: Window,
    stimulus: Stimulus,
    frameRate: float,
    syncSquares: Optional[SyncSquares],
    params: Dict[str, Any] = DEFAULT_PARAMS,
    callback: Any = None,
    shouldTerminate: Any = checkForEsc,
):
    duration = params["stimulus"]["stimulus duration"] or stimulus.duration
    for frameIdx in range(int(frameRate * duration)):
        # check if we should terminate
        if shouldTerminate():
            break

        # execute per-frame callback
        if callback:
            callback()

        # send a sync pulse if needed
        if (
            syncSquares
            and params["sync"]["pulse length"]
            and frameIdx % params["sync"]["sync interval"]
            in {0, params["sync"]["pulse length"]}
        ):
            syncSquares.toggle(0)

        # draw stimulus (+ sync squares)
        stimulus.drawFrame()
        if syncSquares:
            syncSquares.draw()
        window.flip()

    # turn off sync square
    if syncSquares:
        syncSquares.turn_off(0)
        window.flip()
