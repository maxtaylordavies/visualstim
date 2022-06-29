from typing import Any, Dict

import numpy as np
from src.window import Window
from src.constants import (
    DEFAULT_SCREEN_PARAMS,
    DEFAULT_STIMULUS_PARAMS,
)
from src.utils import roundToPowerOf2, scaleUp


def checkerboard(
    window: Window,
    stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
    screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
    logGenerator=None,
):
    if not logGenerator:
        logGenerator = window.reportProgress
    logGenerator([None], f"{stimParams['label']}: generating frames")

    r, c = window.getFrameShape()
    r, c = int(r * stimParams["scale"]), int(c * stimParams["scale"])
    return np.array([2 * (np.indices((r, c)).sum(axis=0) % 2) - 1])
