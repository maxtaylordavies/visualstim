from typing import Any, Dict

import numpy as np
from src.window import Window
from src.constants import (
    DEFAULT_SCREEN_PARAMS,
    DEFAULT_STIMULUS_PARAMS,
)
from src.utils import scaleUp


def checkerboard(
    window: Window,
    stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
    screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
    logGenerator=None,
):
    if not logGenerator:
        logGenerator = window.reportProgress
    logGenerator([None], f"{stimParams['label']}: generating frames")

    (r, c) = window.getFrameShape()
    r, c = r // stimParams["block size"], c // stimParams["block size"]
    return np.array(
        [scaleUp(np.indices((r, c)).sum(axis=0) % 2, stimParams["block size"])]
    )
