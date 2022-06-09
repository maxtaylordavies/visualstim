from typing import Any, Dict
import numpy as np

from src.constants import (
    DEFAULT_SCREEN_PARAMS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    DEFAULT_STIMULUS_PARAMS,
)
from src.utils import normalise, roundToPowerOf2, scaleUp, warpTexture


def sparseNoise(
    frameRate: float,
    stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
    screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
):
    rng = np.random.default_rng()

    nFrames = round(frameRate * stimParams["stim duration"] * stimParams["temp freq"])

    dim = max(WINDOW_WIDTH, WINDOW_HEIGHT)
    n = roundToPowerOf2(dim)
    l = roundToPowerOf2(dim * stimParams["scale"])

    def randomMatrix():
        x = (
            np.inf
            if stimParams["sparseness"] == 1
            else (1 / (1 - stimParams["sparseness"])) - 1
        )
        edges = np.array([-np.inf, -x, x, np.inf])
        return scaleUp(
            normalise(np.digitize(rng.standard_normal((l, l)), edges)), int((n / l) / 2)
        )

    texture = [randomMatrix() for _ in range(nFrames)]
    return (
        warpTexture(texture, screenParams=screenParams)
        if screenParams["warp"]
        else texture
    )

