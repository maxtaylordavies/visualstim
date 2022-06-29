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

    # dim = max(screenParams["h res"], screenParams["v res"])
    # n = roundToPowerOf2(dim) // window.compressionFactor
    # l = roundToPowerOf2(dim * stimParams["scale"])

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
        return normalise(np.digitize(rng.standard_normal((r, c)), edges))

    texture = np.zeros((nFrames, r, c), dtype=np.float16)
    if not logGenerator:
        logGenerator = window.reportProgress
    for i in logGenerator(range(nFrames), f"{stimParams['label']}: generating frames"):
        texture[i] = randomMatrix()

    return texture
