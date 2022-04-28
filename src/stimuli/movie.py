from psychopy.visual import Window
from psychopy.visual.movie3 import MovieStim3

from .stimulus import Stimulus


class Movie(Stimulus):
    def __init__(self, window: Window, path: str) -> None:
        self.window = window
        self._movie = MovieStim3(window, path, noAudio=True)

    def drawFrame(self) -> None:
        self._movie.draw()
