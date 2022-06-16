from typing import Any, Dict

import numpy as np
from src.window import Window
from src.constants import (
    DEFAULT_SCREEN_PARAMS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    DEFAULT_STIMULUS_PARAMS,
)
from src.utils import roundToPowerOf2, scaleUp, ReportProgress


def checkerboard(
    window: Window, stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
):
    ReportProgress([None], window, f"{stimParams['label']}: generating frames")

    dim = max(WINDOW_WIDTH, WINDOW_HEIGHT)
    n = roundToPowerOf2(dim)
    l = roundToPowerOf2(dim * stimParams["scale"])

    return np.array([scaleUp(2 * (np.indices((l, l)).sum(axis=0) % 2) - 1, int(n / l))])
