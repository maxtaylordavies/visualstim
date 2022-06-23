from typing import Dict

from src.window import Window
from src.constants import DEFAULT_STIMULUS_PARAMS, DEFAULT_SCREEN_PARAMS
from src.textures import staticGrating, driftingGrating, oscGrating
from .stimulus import Stimulus


class StaticGrating(Stimulus):
    def __init__(
        self,
        window: Window,
        stimParams: Dict = DEFAULT_STIMULUS_PARAMS,
        screenParams: Dict = DEFAULT_SCREEN_PARAMS,
        logGenerator=None,
    ):
        super().__init__(window, stimParams, screenParams, logGenerator)

    def loadTexture(self):
        self.texture = staticGrating(
            self.window, self.stimParams, self.screenParams, self.logGenerator,
        )

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
            self.window,
            self.stimParams,
            self.screenParams,
            logGenerator=self.logGenerator,
        )

    def updatePhase(self):
        self._stim.tex = self.texture[self.frameIdx % len(self.texture)]


class OscillatingGrating(StaticGrating):
    def loadTexture(self):
        self.texture = oscGrating(
            self.window,
            self.stimParams,
            self.screenParams,
            logGenerator=self.logGenerator,
        )

    def updatePhase(self):
        self._stim.tex = self.texture[self.frameIdx % len(self.texture)]

