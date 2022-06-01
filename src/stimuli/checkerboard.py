from typing import Any, Dict

import numpy as np
from psychopy.visual import Window
from psychopy.visual.grating import GratingStim

from src.constants import WINDOW_WIDTH, DEFAULT_PARAMS
from src.textures import checkerboard
from .stimulus import Stimulus


class Checkerboard(Stimulus):
    def __init__(
        self, window: Window, frameRate: float, params: Dict[str, Any] = DEFAULT_PARAMS
    ):
        super().__init__(window, frameRate, params)

        self.texture = checkerboard(self.params)

        self._stim = GratingStim(
            win=self.window,
            size=[WINDOW_WIDTH, WINDOW_WIDTH],
            units="pix",
            ori=self.params["orientation"],
            tex=self.texture,
        )
        self.drawInterval = int(1 / self.params["temp freq"])

    def drawFrame(self) -> None:
        if self.frameIdx % self.drawInterval == 0:
            self._stim.tex = np.negative(self._stim.tex)
        self._stim.draw()
        self.frameIdx += 1
