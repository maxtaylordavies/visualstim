from typing import Any, Dict

from psychopy.visual import Window
from psychopy.visual.grating import GratingStim

from src.constants import WINDOW_WIDTH, DEFAULT_STIMULUS_PARAMS, DEFAULT_SCREEN_PARAMS
from src.utils import sinDeg, pix2deg
from .stimulus import Stimulus


class StaticGrating(Stimulus):
    def __init__(
        self,
        window: Window,
        frameRate: float,
        stimParams: Dict = DEFAULT_STIMULUS_PARAMS,
    ):
        super().__init__(window, frameRate, stimParams)

        self._stim = GratingStim(
            win=self.window,
            size=[WINDOW_WIDTH, WINDOW_WIDTH],
            units="pix",
            ori=self.stimParams["orientation"],
            tex="sin",
            mask=None,
            phase=0,
            sf=pix2deg(self.stimParams["spat freq"], DEFAULT_SCREEN_PARAMS),
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
        self._stim.phase = (self.frameIdx / self.frameRate) * self.stimParams[
            "temp freq"
        ]


class OscillatingGrating(StaticGrating):
    def updatePhase(self):
        self._stim.phase = sinDeg(
            self.stimParams["temp freq"] * self.frameIdx * (360 / self.frameRate)
        )

