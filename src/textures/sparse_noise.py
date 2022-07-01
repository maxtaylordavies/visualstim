from typing import Any, Dict
import numpy as np

from src.window import Window
from src.constants import (
    DEFAULT_SCREEN_PARAMS,
    DEFAULT_STIMULUS_PARAMS,
)
from src.utils import scaleUp


def sparseNoise(
    window: Window,
    stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
    screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
    logGenerator=None,
):
    rng = np.random.default_rng()

    nFrames = round(
        window.frameRate * stimParams["stim duration"] * stimParams["temp freq"]
    )

    r, c = window.getFrameShape()
    r, c = r // stimParams["block size"], c // stimParams["block size"]

    def randomMatrix():
        x = (
            np.inf
            if stimParams["sparseness"] == 1
            else (1 / (1 - stimParams["sparseness"])) - 1
        )
        edges = np.array([-np.inf, -x, x, np.inf])
        return scaleUp(
            np.digitize(rng.standard_normal((r, c)), edges), stimParams["block size"]
        )

    texture = np.zeros(
        (nFrames, r * stimParams["block size"], c * stimParams["block size"]),
        dtype=np.float16,
    )
    if not logGenerator:
        logGenerator = window.reportProgress
    for i in logGenerator(range(nFrames), f"{stimParams['label']}: generating frames"):
        texture[i] = randomMatrix()

    return texture
