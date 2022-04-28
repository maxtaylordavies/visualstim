from typing import Any, Dict, List, Optional

from psychopy.visual import Window
from psychopy.visual.grating import GratingStim

from src.constants import WINDOW_WIDTH, DEFAULT_PARAMS
from .stimulus import Stimulus


class Grating(Stimulus):
    def __init__(
        self, window: Window, texture: List, params: Dict[str, Any] = DEFAULT_PARAMS
    ):
        self.window = window
        self.texture = texture
        self.params = params
        self.frameIdx = 0
        self._grating = GratingStim(
            win=window,
            size=[WINDOW_WIDTH, WINDOW_WIDTH],
            units="pix",
            ori=params["stimulus"]["orientation"],
        )

    def drawFrame(self) -> None:
        self._grating.tex = self.texture[self.frameIdx % len(self.texture)]
        self._grating.draw()
        self.frameIdx += 1
