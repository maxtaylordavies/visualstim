import pathlib

from psychopy.visual import Window
from psychopy.visual.movie3 import MovieStim3

from src.constants import WINDOW_HEIGHT, WINDOW_WIDTH, GREY
from .stimulus import Stimulus


class Movie(Stimulus):
    def __init__(self, window: Window, filename: str, fitScreen: bool = False) -> None:
        super().__init__()
        size = [WINDOW_WIDTH, WINDOW_HEIGHT] if fitScreen else None
        self._movie = MovieStim3(
            window,
            pathlib.Path().resolve().joinpath(f"movies/{filename}"),
            noAudio=True,
            size=size,
        )
        self.duration = self._movie.duration

    def drawFrame(self) -> None:
        self._movie.draw()
