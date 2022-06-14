import pathlib
from typing import Any, Dict

from psychopy.visual.movie3 import MovieStim3

from src.window import Window
from src.constants import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    DEFAULT_STIMULUS_PARAMS,
    DEFAULT_SCREEN_PARAMS,
)
from .stimulus import Stimulus


class Movie(Stimulus):
    def __init__(
        self,
        window: Window,
        frameRate: float,
        stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
        screenParams: Dict = DEFAULT_SCREEN_PARAMS,
    ) -> None:
        super().__init__(window, frameRate, stimParams, screenParams)

        self._movie = MovieStim3(
            self.window,
            pathlib.Path().resolve().joinpath(f"movies/{self.stimParams['filename']}"),
            noAudio=True,
            size=[WINDOW_WIDTH, WINDOW_HEIGHT]
            if self.stimParams["fit screen"]
            else None,
        )

        self.duration = self._movie.duration

    def drawFrame(self) -> None:
        self._movie.draw()
