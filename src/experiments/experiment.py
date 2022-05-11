import json
import pathlib
from typing import Any, Dict, List, Optional

from psychopy.visual import Window

from src.stimuli import Stimulus, StaticGrating, DriftingGrating, Movie, playStimulus
from src.components import SyncSquares
from src.constants import (
    DEFAULT_PARAMS,
    DEFAULT_BACKGROUND_COLOR,
    STIMULATION_BACKGROUND_COLOR,
)
from src.utils import checkForEsc


def str2Stim(s: str) -> Stimulus:
    return {
        "static grating": StaticGrating,
        "drifting grating": DriftingGrating,
        "movie": Movie,
    }[s]


def createStim(x: Dict, window: Window, frameRate: float) -> Dict:
    return {
        "stimulus": str2Stim(x["name"])(window, frameRate, params=x["params"]),
        "params": x["params"],
    }


class Experiment:
    def __init__(self, name: str, syncSettings: Dict, stimuli: List[Dict]) -> None:
        self.name = name
        self.syncSettings = syncSettings
        self.stimuli = stimuli


def loadExperiment(window: Window, frameRate: float, filename: str) -> None:
    # TODO: check file exists / error handling
    with open(pathlib.Path().resolve().joinpath(f"experiments/{filename}")) as f:
        data = json.load(f)

    return Experiment(data["name"], data["sync settings"], data["stimuli"])


def playExperiment(
    window: Window,
    experiment: Experiment,
    frameRate: float,
    syncSquares: Optional[SyncSquares],
    callback: Any = None,
    shouldTerminate: Any = checkForEsc,
):
    window.color = STIMULATION_BACKGROUND_COLOR

    # create stimuli objects from descriptions
    stimuli = list(map(lambda s: createStim(s, window, frameRate), experiment.stimuli))

    def _callback(frameIdx: int):
        # send a sync pulse if needed
        if (
            syncSquares
            and experiment.syncSettings["pulse length"]
            and frameIdx % experiment.syncSettings["sync interval"]
            in {0, experiment.syncSettings["pulse length"]}
        ):
            syncSquares.toggle(0)
        callback()

    # trigger loop
    if syncSquares:
        syncSquares.toggle(1)  # turn on trigger square
        for i in range(int(frameRate * experiment.syncSettings["trigger duration"])):
            # check if we should terminate
            if shouldTerminate():
                break

            # execute per-frame callback
            if callback:
                callback()

            if i == experiment.syncSettings["pulse length"]:
                syncSquares.toggle(1)  # turn off trigger square

            syncSquares.draw()
            window.flip()

    # cycle through + display stimuli
    for stimulus in stimuli:
        playStimulus(
            window, stimulus, frameRate, syncSquares, _callback, shouldTerminate,
        )
        if syncSquares:
            syncSquares.turn_off(0)
            window.flip()

    # reset window colour
    window.color = DEFAULT_BACKGROUND_COLOR
    window.flip()
