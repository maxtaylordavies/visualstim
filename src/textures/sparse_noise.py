from typing import Any, Dict
import numpy as np

from src.window import Window
from src.constants import (
    COMPRESSION_FACTOR,
    DEFAULT_SCREEN_PARAMS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    DEFAULT_STIMULUS_PARAMS,
)
from src.utils import normalise, roundToPowerOf2, scaleUp, warpTexture, ReportProgress


def sparseNoise(
    window: Window,
    frameRate: float,
    stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
):
    rng = np.random.default_rng()

    nFrames = round(frameRate * stimParams["stim duration"] * stimParams["temp freq"])

    dim = max(WINDOW_WIDTH, WINDOW_HEIGHT)
    n = roundToPowerOf2(dim) // COMPRESSION_FACTOR
    l = roundToPowerOf2(dim * stimParams["scale"])

    def randomMatrix():
        x = (
            np.inf
            if stimParams["sparseness"] == 1
            else (1 / (1 - stimParams["sparseness"])) - 1
        )
        edges = np.array([-np.inf, -x, x, np.inf])
        return scaleUp(
            normalise(np.digitize(rng.standard_normal((l, l)), edges)), (n // l),
        )

    texture = np.zeros((nFrames, n, n), dtype=np.float16)
    for i in ReportProgress(range(nFrames), window, "generating frames"):
        texture[i] = randomMatrix()

    return texture
