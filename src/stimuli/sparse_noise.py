from typing import Any, Dict, List, Optional

import numpy as np
from psychopy.visual import Window
from psychopy.visual.grating import GratingStim

from src.constants import WINDOW_WIDTH, DEFAULT_PARAMS
from src.textures import sparseNoise
from .stimulus import Stimulus


class SparseNoise(Stimulus):
    def __init__(
        self, window: Window, frameRate: float, params: Dict[str, Any] = DEFAULT_PARAMS
    ):
        super().__init__(window, frameRate, params)

        self.texture = sparseNoise(self.frameRate, self.params)

        print([np.max(self.texture[0]), np.min(self.texture[0])])

        self._stim = GratingStim(
            win=self.window,
            size=[WINDOW_WIDTH, WINDOW_WIDTH],
            units="pix",
            ori=self.params["orientation"],
        )
        self.drawInterval = int(1 / self.params["temporal frequency"])

    def drawFrame(self) -> None:
        if self.frameIdx % self.drawInterval == 0:
            self._stim.tex = self.texture[
                int(self.frameIdx * self.params["temporal frequency"])
                % len(self.texture)
            ]
        self._stim.draw()
        self.frameIdx += 1
