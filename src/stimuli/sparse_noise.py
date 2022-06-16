from typing import Any, Dict

from src.window import Window
from src.constants import DEFAULT_STIMULUS_PARAMS, DEFAULT_SCREEN_PARAMS
from src.textures import sparseNoise
from .stimulus import Stimulus


class SparseNoise(Stimulus):
    def __init__(
        self,
        window: Window,
        frameRate: float,
        stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
        screenParams: Dict = DEFAULT_SCREEN_PARAMS,
    ):
        super().__init__(window, frameRate, stimParams, screenParams)
        self.drawInterval = int(1 / self.stimParams["temp freq"])

    def loadTexture(self) -> None:
        self.texture = sparseNoise(
            self.window, self.frameRate, self.stimParams, self.screenParams
        )

    def drawFrame(self) -> None:
        if self.frameIdx % self.drawInterval == 0:
            self._stim.tex = self.texture[
                int(self.frameIdx * self.stimParams["temp freq"]) % len(self.texture)
            ]
        self._stim.draw()
        self.frameIdx += 1
