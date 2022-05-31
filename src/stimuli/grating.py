from typing import Any, Dict

from psychopy.visual import Window
from psychopy.visual.grating import GratingStim

from src.constants import WINDOW_WIDTH, DEFAULT_PARAMS
from src.utils import sinDeg
from .stimulus import Stimulus


class StaticGrating(Stimulus):
    def __init__(
        self, window: Window, frameRate: float, params: Dict[str, Any] = DEFAULT_PARAMS
    ):
        super().__init__(window, frameRate, params)

        self._stim = GratingStim(
            win=self.window,
            size=[WINDOW_WIDTH, WINDOW_WIDTH],
            units="pix",
            ori=self.params["orientation"],
            tex="sin",
            mask=None,
            phase=0,
            sf=self.params["spatial frequency"],
        )

    def updatePhase(self):
        pass

    def drawFrame(self) -> None:
        # draw the grating to the screen
        self._stim.draw()

        # update the phase of the grating in order to drift it
        self.updatePhase()

        # increment frame counter
        self.frameIdx += 1


class DriftingGrating(StaticGrating):
    def updatePhase(self):
        self._stim.phase = (self.frameIdx / self.frameRate) * self.params[
            "temporal frequency"
        ]


class OscillatingGrating(StaticGrating):
    def updatePhase(self):
        self._stim.phase = sinDeg(
            self.params["temporal frequency"] * self.frameIdx * (360 / self.frameRate)
        )

