from datetime import datetime
from math import degrees, atan2
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union
import itertools
import socket

import numpy as np
import scipy.ndimage.interpolation as spndi
from psychopy import event
from pyglet.canvas import get_display

# from src.window import Window
from src.constants import (
    DEFAULT_SCREEN_PARAMS,
    DEFAULT_STIMULUS_PARAMS,
    PARAMETER_UNITS_MAP,
)


def log(message: str) -> None:
    print(f"{datetime.now()}: {message}")


def checkForEsc() -> bool:
    return "escape" in event.getKeys()


def noOp(args: Any) -> None:
    return


def parseParams(params: Dict) -> Dict:
    return {
        k: params[k] if k in params else DEFAULT_STIMULUS_PARAMS[k]
        for k in DEFAULT_STIMULUS_PARAMS.keys()
    }


def normalise(x: np.ndarray) -> np.ndarray:
    # normalise x to within the range [-1, 1]
    return np.nan_to_num((2 * (x - np.min(x)) / (np.max(x) - np.min(x))) - 1)


def scaleUp(x: np.ndarray, factor: int) -> np.ndarray:
    return np.kron(x, np.ones((factor, factor)))


def sinDeg(x):
    return np.sin(np.radians(x))


def roundToPowerOf2(x: float) -> int:
    # adapted from https://graphics.stanford.edu/~seander/bithacks.html#RoundUpPowerOf2
    x = int(x) - 1
    for e in [1, 2, 4, 8, 16]:
        x |= x >> e
    return x + 1


def paramLabelWithUnits(key: str) -> str:
    return f"{key} ({PARAMETER_UNITS_MAP[key]})" if key in PARAMETER_UNITS_MAP else key


def deg2pix(pix, screenParams):
    return (
        pix
        * degrees(atan2(screenParams["height"] / 2, screenParams["dist"]))
        / (screenParams["v res"] / 2)
    )


def getScreenResolution(screenNum: int) -> List[int]:
    screens = get_display().get_screens()
    if screenNum >= len(screens):
        raise Exception("screenNum too high")
    return [screens[screenNum].width, screens[screenNum].height]


def computeWarpCoords(shape: tuple, screenParams: Dict) -> np.ndarray:
    vRes, hRes = shape
    x = np.array(range(hRes), dtype=np.float32) - hRes / 2
    y = np.array(range(vRes), dtype=np.float32) - vRes / 2
    vertices = np.array(list(itertools.product(y, x)), dtype=np.float32)

    mon_width_cm = float(screenParams["width"] / 10)
    mon_height_cm = float(screenParams["height"] / 10)
    distance = float(screenParams["dist"] / 10)
    eyepoint = (0.5, 0.5)

    # from pixels (-1920/2 -> 1920/2) to stimulus space (-0.5->0.5)
    vertices[:, 0] = vertices[:, 0] / hRes
    vertices[:, 1] = vertices[:, 1] / vRes

    x = (vertices[:, 0] + 0.5) * mon_width_cm
    y = (vertices[:, 1] + 0.5) * mon_height_cm

    xEye = eyepoint[0] * mon_width_cm
    yEye = eyepoint[1] * mon_height_cm

    x = x - xEye
    y = y - yEye

    r = np.sqrt(np.square(x) + np.square(y) + np.square(distance))

    azimuth = np.arctan(x / distance)
    altitude = np.arcsin(y / r)

    # calculate the texture coordinates
    tx = distance * (1 + x / r) - distance
    ty = distance * (1 + y / r) - distance

    # prevent div0
    azimuth[azimuth == 0] = np.finfo(np.float32).eps
    altitude[altitude == 0] = np.finfo(np.float32).eps

    # the texture coordinates (which are now lying on the sphere)
    # need to be remapped back onto the plane of the display.
    # This effectively stretches the coordinates away from the eyepoint.

    centralAngle = np.arccos(np.cos(altitude) * np.cos(np.abs(azimuth)))
    # distance from eyepoint to texture vertex
    arcLength = centralAngle * distance
    # remap the texture coordinate
    theta = np.arctan2(ty, tx)
    tx = arcLength * np.cos(theta)
    ty = arcLength * np.sin(theta)

    u_coords = tx / mon_width_cm
    v_coords = ty / mon_height_cm

    warpCoords = np.column_stack((u_coords, v_coords))

    # back to pixels
    warpCoords[:, 0] = warpCoords[:, 0] * hRes
    warpCoords[:, 1] = warpCoords[:, 1] * vRes
    warpCoords[:, 0] += vRes / 2
    warpCoords[:, 1] += hRes / 2

    return warpCoords


def warpTexture(
    window: Any,
    texture: np.ndarray,
    screenParams: Dict = DEFAULT_SCREEN_PARAMS,
    label: str = "",
    logGenerator=None,
) -> np.ndarray:

    shape = texture[0].shape
    warpCoords = computeWarpCoords(shape, screenParams)

    desc = "applying spherical warp"
    if label:
        desc = f"{label}: {desc}"

    if not logGenerator:
        logGenerator = window.reportProgress

    warped = np.zeros(texture.shape, dtype=np.float32)
    for i in logGenerator(range(len(texture)), desc):
        warped[i] = spndi.map_coordinates(texture[i], warpCoords.T).reshape(shape)

    return warped


def rgb2grey(x: np.ndarray) -> np.ndarray:
    return np.dot(x[..., :3], [0.2989, 0.5870, 0.1140])


def padWithGrey(x: np.ndarray, shape: Iterable) -> np.ndarray:
    diffs = [(shape[i] - x.shape[i]) // 2 for i in range(len(x.shape))]
    padWidth = [(d, d) for d in diffs]
    return np.pad(x, padWidth)
