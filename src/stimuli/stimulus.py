from datetime import datetime
from typing import Any, Dict

import numpy as np
from psychopy.visual.grating import GratingStim

from src.window import Window
from src.constants import DEFAULT_SCREEN_PARAMS, DEFAULT_STIMULUS_PARAMS
from src.utils import checkForEsc, warpTexture


class Stimulus:
    def __init__(
        self,
        window: Window,
        stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
        screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
        logGenerator=None,
        duration=0,
    ) -> None:
        self.window = window
        self.stimParams = stimParams
        self.screenParams = screenParams
        self.logGenerator = logGenerator or window.reportProgress
        self.duration = duration
        self.frameIdx = 0
        self.updateInterval = 1

        # for logging purposes
        if "label" not in self.stimParams:
            self.stimParams["label"] = "stimulus 1/1"

        self.loadTexture()
        print(f"TEXTURE SHAPE = {self.texture.shape}")
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
            self.logGenerator,
        ).astype(np.float16)

    def setUpdateInterval(self, updateInterval) -> None:
        self.updateInterval = updateInterval

    def drawFrame(self) -> None:
        self._stim.draw()

    def updateFrame(self) -> None:
        idx = int(self.frameIdx / self.updateInterval)
        self._stim.tex = self.texture[idx % len(self.texture)]


def playStimulus(
    window: Window,
    stimulus: Dict,
    callback: Any = None,
    shouldTerminate: Any = checkForEsc,
    experimentFrameIdx: int = 0,
) -> bool:
    duration = stimulus["stimulus"].duration or stimulus["params"]["stim duration"]
    print(f"duration = {duration}")

    stimulus["stimulus"].frameIdx = experimentFrameIdx

    startTime = datetime.now()

    while stimulus["stimulus"].frameIdx < experimentFrameIdx + int(
        window.frameRate * duration
    ):
        # check if we should terminate
        if shouldTerminate():
            return True, stimulus["stimulus"].frameIdx + 1

        # execute per-frame callback
        if callback:
            callback(stimulus["stimulus"].frameIdx)

        # draw stimulus
        stimulus["stimulus"].drawFrame()
        window.flip()

        # update frame
        stimulus["stimulus"].frameIdx += 1
        if stimulus["stimulus"].frameIdx % stimulus["stimulus"].updateInterval == 0:
            stimulus["stimulus"].updateFrame()

    print(f"FINISHED AFTER {datetime.now() - startTime}")

    return False, stimulus["stimulus"].frameIdx + 1
