from typing import Any, Dict, List
import numpy as np

from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_STIMULUS_PARAMS
from src.utils import roundToPowerOf2, scaleUp, warpTexture


def checkerboard(params: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS):
    l = roundToPowerOf2(max(WINDOW_WIDTH, WINDOW_HEIGHT) * params["scale"])
    return 2 * (np.indices((l, l)).sum(axis=0) % 2) - 1
