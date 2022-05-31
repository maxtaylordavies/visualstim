from typing import Any, Dict, List
import numpy as np

from src.constants import WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_PARAMS
from src.utils import normalise


def checkerboard(params: Dict[str, Any] = DEFAULT_PARAMS):
    l = int(max(WINDOW_WIDTH, WINDOW_HEIGHT) * params["scale"])
    return 2 * (np.indices((l, l)).sum(axis=0) % 2) - 1
