from typing import Any, Dict
import numpy as np

from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_PARAMS
from src.utils import normalise


def sparseNoise(frameRate: float, params: Dict[str, Any] = DEFAULT_PARAMS):
    rng = np.random.default_rng()

    nFrames = round(
        frameRate * params["stimulus duration"] * params["temporal frequency"]
    )

    l = int(max(WINDOW_WIDTH, WINDOW_HEIGHT) * params["scale"])

    def randomMatrix():
        x = (
            np.inf
            if params["sparseness"] == 1
            else (1 / (1 - params["sparseness"])) - 1
        )
        edges = np.array([-np.inf, -x, x, np.inf])
        return normalise(np.digitize(rng.standard_normal((l, l)), edges))

    return [randomMatrix() for _ in range(nFrames)]

