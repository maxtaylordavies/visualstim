from typing import Any, Dict

import numpy as np

from src.window import Window
from src.constants import (
    DEFAULT_SCREEN_PARAMS,
    DEFAULT_STIMULUS_PARAMS,
)
from src.utils import sinDeg, deg2pix


def gratingFrame(r: int, c: int, sf: float, phase: float) -> np.ndarray:
    return np.tile(sinDeg((360 * sf * np.arange(c)) + phase), (r, 1))


def computeShape(window: Window, ori: float):
    r, c = window.getFrameShape()
    r, c = r // window.compressionFactor, c // window.compressionFactor

    if ori != 0:
        r = c = round(((r ** 2) + (c ** 2)) ** 0.5)

    return r, c


def staticGrating(
    window: Window,
    stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
    screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
    logGenerator=None,
):
    r, c = computeShape(window, stimParams["orientation"])
    sf = deg2pix(stimParams["spat freq"], screenParams) * window.compressionFactor
    return np.array([gratingFrame(r, c, sf, 0)])


def driftingGrating(
    window: Window,
    stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
    screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
    logGenerator=None,
):
    r, c = computeShape(window, stimParams["orientation"])
    sf = deg2pix(stimParams["spat freq"], screenParams) * window.compressionFactor

    # we first need to figure out how many frames we need to generate
    # only need to generate enough frames for 1 cycle, since after that
    # the frames just repeat
    nFrames = round(window.frameRate / stimParams["temp freq"])

    # then we need to compute the *phase* of each frame as a function
    # of frame index, framerate and temporal frequency
    # 1 cycle = 360 degrees of phase - so if we're at 1Hz then we need
    # to increase phase at a rate of 360 degrees per second
    # -> need to increase phase at a rate of (360 * tf) degrees / second
    # and we have fr frames per second -> need to increase phase at a rate
    # of (360 * tf / fr) degrees per frame
    phases = (360 * stimParams["temp freq"] / window.frameRate) * np.arange(nFrames)

    # then we map the array of phases to an array of frames
    texture = np.zeros((nFrames, r, c), dtype=np.float16)
    if not logGenerator:
        logGenerator = window.reportProgress
    for i in logGenerator(range(nFrames), f"{stimParams['label']}: generating frames"):
        texture[i] = gratingFrame(r, c, sf, phases[i])

    return texture


def oscGrating(
    window: Window,
    stimParams: Dict[str, Any] = DEFAULT_STIMULUS_PARAMS,
    screenParams: Dict[str, Any] = DEFAULT_SCREEN_PARAMS,
    logGenerator=None,
):
    r, c = computeShape(window, stimParams["orientation"])
    sf = deg2pix(stimParams["spat freq"], screenParams) * window.compressionFactor
    nFrames = round(window.frameRate / stimParams["temp freq"])

    phases = 360 * sinDeg(
        (360 * stimParams["temp freq"] / window.frameRate) * np.arange(nFrames)
    )

    texture = np.zeros((nFrames, r, c), dtype=np.float16)
    if not logGenerator:
        logGenerator = window.reportProgress
    for i in logGenerator(range(nFrames), f"{stimParams['label']}: generating frames"):
        texture[i] = gratingFrame(r, c, sf, phases[i])

    return texture
