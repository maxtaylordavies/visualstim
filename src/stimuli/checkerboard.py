from typing import Any, Dict

import numpy as np
from psychopy.visual.grating import GratingStim

from src.window import Window
from src.constants import WINDOW_WIDTH, DEFAULT_STIMULUS_PARAMS, DEFAULT_SCREEN_PARAMS
from src.textures import checkerboard
from .stimulus import Stimulus


class Checkerboard(Stimulus):
    def __init__(
        self,
        window: Window,
        frameRate: float,
        stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
        screenParams: Dict = DEFAULT_SCREEN_PARAMS,
    ):
        super().__init__(window, frameRate, stimParams, screenParams)

        self.texture = checkerboard(self.window, self.stimParams, self.screenParams)

        self._stim = GratingStim(
            win=self.window,
            size=[WINDOW_WIDTH, WINDOW_WIDTH],
            units="pix",
            ori=self.stimParams["orientation"],
            tex=self.texture,
        )
        self.drawInterval = int(1 / self.stimParams["temp freq"])

    def drawFrame(self) -> None:
        if self.frameIdx % self.drawInterval == 0:
            self._stim.tex = np.negative(self._stim.tex)
        self._stim.draw()
        self.frameIdx += 1
