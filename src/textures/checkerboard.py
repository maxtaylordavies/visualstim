from typing import Any, Dict
import numpy as np

from src.constants import (
    DEFAULT_SCREEN_PARAMS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    DEFAULT_STIMULUS_PARAMS,
)
from src.utils import roundToPowerOf2, scaleUp, warpTexture


def checkerboard(
    stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
    screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
):
    dim = max(WINDOW_WIDTH, WINDOW_HEIGHT)
    n = roundToPowerOf2(dim)
    l = roundToPowerOf2(dim * stimParams["scale"])

    checkerboard = scaleUp(2 * (np.indices((l, l)).sum(axis=0) % 2) - 1, int(n / l))
    return (
        warpTexture([checkerboard], screenParams=screenParams)[0]
        if screenParams["warp"]
        else checkerboard
    )
