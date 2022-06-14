from typing import Any, Dict, List, Optional

from src.window import Window
from src.components import SyncSquares
from src.constants import DEFAULT_SCREEN_PARAMS, DEFAULT_STIMULUS_PARAMS
from src.utils import checkForEsc, log


class Stimulus:
    def __init__(
        self,
        window: Window,
        frameRate: float,
        stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
        screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
    ) -> None:
        self.window = window
        self.frameRate = frameRate
        self.stimParams = stimParams
        self.screenParams = screenParams
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
) -> bool:
    duration = stimulus["params"]["stim duration"] or stimulus.duration
    for frameIdx in range(int(frameRate * duration)):
        # check if we should terminate
        if shouldTerminate():
            return True

        # execute per-frame callback
        if callback:
            callback(frameIdx)

        # draw stimulus (+ sync squares)
        stimulus["stimulus"].drawFrame()
        if syncSquares:
            syncSquares.draw()

        window.flip()

    return False
