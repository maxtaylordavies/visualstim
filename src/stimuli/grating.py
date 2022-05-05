from typing import Any, Dict, List, Optional

from psychopy.visual import Window
from psychopy.visual.grating import GratingStim

from src.constants import WINDOW_WIDTH, DEFAULT_PARAMS
from src.textures import drumTexture
from .stimulus import Stimulus


class Grating(Stimulus):
    def __init__(
        self, window: Window, frameRate: float, params: Dict[str, Any] = DEFAULT_PARAMS
    ):
        super().__init__(window, frameRate, params)
        self.texture = drumTexture(self.frameRate, self.params)
        self._grating = GratingStim(
            win=self.window,
            size=[WINDOW_WIDTH, WINDOW_WIDTH],
            units="pix",
            ori=self.params["stimulus"]["orientation"],
        )

    def drawFrame(self) -> None:
        self._grating.tex = self.texture[self.frameIdx % len(self.texture)]
        self._grating.draw()
        self.frameIdx += 1
