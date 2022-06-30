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


class DriftingGrating(StaticGrating):
    def loadTexture(self):
        self.texture = driftingGrating(
            self.window,
            self.stimParams,
            self.screenParams,
            logGenerator=self.logGenerator,
        )


class OscillatingGrating(StaticGrating):
    def loadTexture(self):
        self.texture = oscGrating(
            self.window,
            self.stimParams,
            self.screenParams,
            logGenerator=self.logGenerator,
        )

