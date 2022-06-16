from typing import Any, Dict, Optional

import numpy as np
from psychopy.visual.grating import GratingStim

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
        self.duration = 0
        self.frameIdx = 0

        # for logging purposes
        if "label" not in self.stimParams:
            self.stimParams["label"] = "stimulus 1/1"

        self.loadTexture()
        if self.screenParams["warp"]:
            self.applyWarp()

        self._stim = GratingStim(
            win=self.window,
            size=[self.screenParams["h res"], self.screenParams["h res"]],
            units="pix",
            ori=self.stimParams["orientation"],
            tex=self.texture[0],
        )

    def loadTexture(self) -> None:
        self.texture = [None]

    def applyWarp(self) -> None:
        if type(self.texture) != np.ndarray:
            return
        self.texture = warpTexture(
            self.window,
            self.texture.astype(np.float32),
            self.screenParams,
            self.stimParams["label"],
        ).astype(np.float16)

    def drawFrame(self) -> None:
        pass


def playStimulus(
    window: Window,
    stimulus: Dict,
    frameRate: float,
    syncSquares: Optional[SyncSquares],
    callback: Any = None,
    shouldTerminate: Any = checkForEsc,
    experimentFrameIdx: int = 0,
) -> bool:
    duration = stimulus["params"]["stim duration"] or stimulus.duration
    for frameIdx in range(
        experimentFrameIdx, experimentFrameIdx + int(frameRate * duration)
    ):
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

    return False, frameIdx + 1
