from typing import Any, Dict, List
import numpy as np

from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_PARAMS
from src.utils import normalise


def checkerboard(params: Dict[str, Any] = DEFAULT_PARAMS):
    width, height = (
        int(WINDOW_WIDTH * params["scale"]),
        int(WINDOW_HEIGHT * params["scale"]),
    )

    m = np.ones((height, width))
    for i in range(height):
        for j in range(width):
            if (i + j) % 2 == 0:
                m[i, j] = -1

    return m
