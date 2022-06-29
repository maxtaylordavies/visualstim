from typing import Any, Dict
import numpy as np

from src.window import Window
from src.constants import (
    DEFAULT_SCREEN_PARAMS,
    DEFAULT_STIMULUS_PARAMS,
)
from src.utils import normalise, roundToPowerOf2, scaleUp


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
    r, c = int(r * stimParams["scale"]), int(c * stimParams["scale"])
    print(f"r, c = {r}, {c}")

    def randomMatrix():
        x = (
            np.inf
            if stimParams["sparseness"] == 1
            else (1 / (1 - stimParams["sparseness"])) - 1
        )
        edges = np.array([-np.inf, -x, x, np.inf])
        return np.digitize(rng.standard_normal((r, c)), edges)

    texture = np.zeros((nFrames, r, c), dtype=np.float16)
    if not logGenerator:
        logGenerator = window.reportProgress
    for i in logGenerator(range(nFrames), f"{stimParams['label']}: generating frames"):
        texture[i] = randomMatrix()

    return texture
