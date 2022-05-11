from typing import Any, Dict, List, Optional

from psychopy.visual import Window

from src.components import SyncSquares
from src.constants import DEFAULT_PARAMS
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


def playStimulus(
    window: Window,
    stimulus: Dict,
    frameRate: float,
    syncSquares: Optional[SyncSquares],
    callback: Any = None,
    shouldTerminate: Any = checkForEsc,
):
    duration = stimulus["params"]["stimulus duration"] or stimulus.duration
    for frameIdx in range(int(frameRate * duration)):
        # check if we should terminate
        if shouldTerminate():
            break

        # execute per-frame callback
        if callback:
            callback(frameIdx)

        # draw stimulus (+ sync squares)
        stimulus["stimulus"].drawFrame()
        if syncSquares:
            syncSquares.draw()
        window.flip()
