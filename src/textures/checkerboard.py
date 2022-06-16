from typing import Any, Dict

import numpy as np
from src.window import Window
from src.constants import (
    DEFAULT_SCREEN_PARAMS,
    DEFAULT_STIMULUS_PARAMS,
)
from src.utils import roundToPowerOf2, scaleUp, ReportProgress


def checkerboard(
    window: Window,
    stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
    screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
):
    ReportProgress([None], window, f"{stimParams['label']}: generating frames")

    dim = max(screenParams["v res"], screenParams["h res"])
    n = roundToPowerOf2(dim)
    l = roundToPowerOf2(dim * stimParams["scale"])

    return np.array([scaleUp(2 * (np.indices((l, l)).sum(axis=0) % 2) - 1, int(n / l))])
