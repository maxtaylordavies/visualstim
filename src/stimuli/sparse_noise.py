from typing import Any, Dict

from src.window import Window
from src.constants import DEFAULT_STIMULUS_PARAMS, DEFAULT_SCREEN_PARAMS
from src.textures import sparseNoise
from .stimulus import Stimulus


class SparseNoise(Stimulus):
    def __init__(
        self,
        window: Window,
        stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
        screenParams: Dict = DEFAULT_SCREEN_PARAMS,
        logGenerator=None,
    ):
        super().__init__(window, stimParams, screenParams, logGenerator)
        self.setUpdateInterval(int(1 / self.stimParams["temp freq"]))

    def loadTexture(self) -> None:
        self.texture = sparseNoise(
            self.window, self.stimParams, self.screenParams, self.logGenerator,
        )
