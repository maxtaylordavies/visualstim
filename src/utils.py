from typing import Any, Dict

import numpy as np
from psychopy import event

from src.constants import DEFAULT_PARAMS


def checkForEsc():
    return "escape" in event.getKeys()


def noOp(args: Any):
    return


def parseParams(params: Dict):
    return {
        k: params[k] if k in params else DEFAULT_PARAMS[k]
        for k in DEFAULT_PARAMS.keys()
    }


def normalise(x):
    # normalise x to within the range [-1, 1]
    return np.nan_to_num((2 * (x - np.min(x)) / (np.max(x) - np.min(x))) - 1)
