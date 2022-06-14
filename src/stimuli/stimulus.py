from typing import Any, Dict, List, Optional

import numpy as np

from src.window import Window
from src.components import SyncSquares
from src.constants import DEFAULT_SCREEN_PARAMS, DEFAULT_STIMULUS_PARAMS
from src.utils import checkForEsc, warpTexture


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
        self.texture = None
        self.duration = 0
        self.frameIdx = 0

        self.loadTexture()
        if self.screenParams["warp"]:
            self.applyWarp()

    def loadTexture(self) -> None:
        pass

    def drawFrame(self) -> None:
        pass

    def applyWarp(self) -> None:
        if self.texture is None:
            return
        self.texture = warpTexture(
            self.window, self.texture.astype(np.float32), self.screenParams
        ).astype(np.float16)


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
