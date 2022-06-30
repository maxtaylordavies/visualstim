import pathlib
from typing import Any, Dict

import numpy as np
from psychopy.visual.movie3 import MovieStim3
from moviepy.video.io.ffmpeg_reader import FFMPEG_VideoReader

from src.window import Window
from src.constants import (
    DEFAULT_STIMULUS_PARAMS,
    DEFAULT_SCREEN_PARAMS,
)
from .stimulus import Stimulus
from src.utils import rgb2grey, normalise, padWithGrey


class Movie(Stimulus):
    def __init__(
        self,
        window: Window,
        stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
        screenParams: Dict = DEFAULT_SCREEN_PARAMS,
        logGenerator=None,
    ) -> None:
        super().__init__(window, stimParams, screenParams, logGenerator)

        self._movie = MovieStim3(
            self.window,
            pathlib.Path().resolve().joinpath(f"movies/{self.stimParams['filename']}"),
            noAudio=True,
            size=[screenParams["h res"], screenParams["v res"]]
            if self.stimParams["fit screen"]
            else None,
        )

        self.duration = self._movie.duration

    def drawFrame(self) -> None:
        self._movie.draw()


class Movie2(Stimulus):
    def __init__(
        self,
        window: Window,
        stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
        screenParams: Dict = DEFAULT_SCREEN_PARAMS,
        logGenerator=None,
    ) -> None:
        self.reader = FFMPEG_VideoReader(
            str(pathlib.Path().resolve().joinpath(f"movies/{stimParams['filename']}")),
            target_resolution=None,
        )
        self.nframes = self.reader.nframes
        super().__init__(
            window, stimParams, screenParams, logGenerator, self.reader.duration
        )
        self.setUpdateInterval(
            round((self.duration * self.window.frameRate) / self.nframes)
        )

    def loadTexture(self) -> None:
        self.texture = np.array(
            [
                rgb2grey(self.reader.read_frame())[::-1]
                for _ in self.logGenerator(
                    range(self.nframes),
                    f"{self.stimParams['label']}: generating frames",
                )
            ]
        )
