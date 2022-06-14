from typing import Dict

from psychopy.visual.grating import GratingStim

from src.window import Window
from src.constants import WINDOW_WIDTH, DEFAULT_STIMULUS_PARAMS, DEFAULT_SCREEN_PARAMS
from src.textures import staticGrating, driftingGrating, oscGrating
from .stimulus import Stimulus


class StaticGrating(Stimulus):
    def __init__(
        self,
        window: Window,
        frameRate: float,
        stimParams: Dict = DEFAULT_STIMULUS_PARAMS,
        screenParams: Dict = DEFAULT_SCREEN_PARAMS,
    ):
        super().__init__(window, frameRate, stimParams, screenParams)

        self.loadTexture()

        self._stim = GratingStim(
            win=self.window,
            size=[WINDOW_WIDTH, WINDOW_WIDTH],
            units="pix",
            ori=self.stimParams["orientation"],
            # tex="sin",
            tex=self.texture[0],
            mask=None,
            # phase=0,
            # sf=deg2pix(self.stimParams["spat freq"], screenParams),
        )

    def loadTexture(self):
        self.texture = staticGrating(self.stimParams, self.screenParams)

    def updatePhase(self):
        pass

    def drawFrame(self) -> None:
        # draw the grating to the screen
        self._stim.draw()

        # increment frame counter
        self.frameIdx += 1

        # update the phase of the grating in order to drift it
        self.updatePhase()


class DriftingGrating(StaticGrating):
    def loadTexture(self):
        self.texture = driftingGrating(
            self.window, self.frameRate, self.stimParams, self.screenParams
        )

    def updatePhase(self):
        self._stim.tex = self.texture[self.frameIdx % len(self.texture)]


class OscillatingGrating(StaticGrating):
    def loadTexture(self):
        self.texture = oscGrating(
            self.window, self.frameRate, self.stimParams, self.screenParams
        )

    def updatePhase(self):
        self._stim.tex = self.texture[self.frameIdx % len(self.texture)]

