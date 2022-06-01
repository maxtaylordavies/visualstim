from datetime import datetime
from typing import Any, Dict

import numpy as np
from psychopy import event

from src.constants import DEFAULT_PARAMS, UNITS_MAP


def log(message: str) -> None:
    print(f"{datetime.now()}: {message}")


def checkForEsc() -> bool:
    return "escape" in event.getKeys()


def noOp(args: Any) -> None:
    return


def parseParams(params: Dict) -> Dict:
    return {
        k: params[k] if k in params else DEFAULT_PARAMS[k]
        for k in DEFAULT_PARAMS.keys()
    }


def normalise(x: np.ndarray) -> np.ndarray:
    # normalise x to within the range [-1, 1]
    return np.nan_to_num((2 * (x - np.min(x)) / (np.max(x) - np.min(x))) - 1)


def sinDeg(x: float) -> float:
    return np.sin(x * np.pi / 180)


def roundToPowerOf2(x: float) -> int:
    # adapted from https://graphics.stanford.edu/~seander/bithacks.html#RoundUpPowerOf2
    x = int(x) - 1
    for e in [1, 2, 4, 8, 16]:
        x |= x >> e
    return x + 1


def paramLabelWithUnits(key: str) -> str:
    return f"{key} ({UNITS_MAP[key]})" if key in UNITS_MAP else key
