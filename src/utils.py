from typing import Any, Dict, List
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
