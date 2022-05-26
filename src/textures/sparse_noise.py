from typing import Any, Dict, List
import numpy as np


from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_PARAMS
from src.utils import normalise


def sparseNoise(frameRate: float, params: Dict[str, Any] = DEFAULT_PARAMS):
    rng = np.random.default_rng()
    nFrames = round(
        frameRate * params["stimulus duration"] * params["temporal frequency"]
    )

    width, height = (
        int(WINDOW_WIDTH * params["scale"]),
        int(WINDOW_HEIGHT * params["scale"]),
    )

    def randomMatrix():
        x = (
            np.inf
            if params["sparseness"] == 1
            else (1 / (1 - params["sparseness"])) - 1
        )
        edges = np.array([-np.inf, -x, x, np.inf])
        return normalise(np.digitize(rng.standard_normal((height, width)), edges))

    return [randomMatrix() for _ in range(nFrames)]

