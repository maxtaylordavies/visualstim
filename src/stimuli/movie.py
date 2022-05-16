import pathlib
from typing import Any, Dict

from psychopy.visual import Window
from psychopy.visual.movie3 import MovieStim3

from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH, DEFAULT_PARAMS
from .stimulus import Stimulus


class Movie(Stimulus):
    def __init__(
        self, window: Window, frameRate: float, params: Dict[str, Any] = DEFAULT_PARAMS
    ) -> None:
        super().__init__(window, frameRate, params)

        size = [WINDOW_WIDTH, WINDOW_HEIGHT] if self.params["fit screen"] else None

        self._movie = MovieStim3(
            self.window,
            pathlib.Path().resolve().joinpath(f"movies/{self.params['filename']}"),
            noAudio=True,
            size=[WINDOW_WIDTH, WINDOW_HEIGHT] if fitScreen else None,
        )

        self.duration = self._movie.duration

    def drawFrame(self) -> None:
        self._movie.draw()
