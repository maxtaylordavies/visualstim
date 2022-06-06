from datetime import datetime
import itertools
import json
import pathlib
from typing import Any, Dict, List, Optional

from psychopy.visual import Window

from src.stimuli import (
    Stimulus,
    StaticGrating,
    DriftingGrating,
    OscillatingGrating,
    SparseNoise,
    Movie,
    Checkerboard,
    playStimulus,
)
from src.components import SyncSquares
from src.constants import (
    DEFAULT_BACKGROUND_COLOR,
    STIMULATION_BACKGROUND_COLOR,
)
from src.utils import checkForEsc, parseParams


def str2Stim(s: str) -> Stimulus:
    return {
        "static grating": StaticGrating,
        "drift grating": DriftingGrating,
        "osc grating": OscillatingGrating,
        "movie": Movie,
        "sparse noise": SparseNoise,
        "checkerboard": Checkerboard,
    }[s]


def createStim(x: Dict, window: Window, frameRate: float, screenSettings: Dict) -> Dict:
    return {
        "stimulus": str2Stim(x["name"])(
            window, frameRate, stimParams=x["params"], screenParams=screenSettings
        ),
        "params": x["params"],
    }


class Experiment:
    def __init__(
        self, name: str, screenSettings: Dict, syncSettings: Dict, stimuli: List[Dict]
    ) -> None:
        self.name = name
        self.screenSettings = screenSettings
        self.syncSettings = syncSettings
        self.stimuli = stimuli

    def toDict(self):
        return {"sync settings": self.syncSettings, "stimuli": self.stimuli}


def loadExperiment(window: Window, frameRate: float, filename: str) -> Experiment:
    # TODO: check file exists / error handling
    with open(pathlib.Path().resolve().joinpath(f"experiments/{filename}")) as f:
        data = json.load(f)

    return Experiment(
        filename,
        data["screen settings"],
        data["sync settings"],
        list(
            map(
                lambda s: {"name": s["name"], "params": parseParams(s["params"])},
                data["stimuli"],
            )
        ),
    )


def saveExperiment(exp: Experiment, filename=""):
    if not filename:
        filename = f"{str(datetime.now())[:19].replace(' ', '_')}.json"
    with open(
        pathlib.Path().resolve().joinpath("experiments").joinpath(filename), "w"
    ) as f:
        json.dump(unrollExperiment(exp).toDict(), f, indent=4)


def unrollExperiment(exp: Experiment) -> Experiment:
    params = parseParams(exp.stimuli[0]["params"])
    listKeys = [k for k, v in params.items() if type(v) == list]

    if not listKeys:
        return exp

    stimuli = []
    for combo in itertools.product(*[params[k] for k in listKeys]):
        stimuli.append(
            {
                "name": exp.stimuli[0]["name"],
                "params": {
                    **params,
                    **{listKeys[i]: combo[i] for i in range(len(listKeys))},
                },
            }
        )

    return Experiment(exp.name, exp.screenSettings, exp.syncSettings, stimuli)


def playExperiment(
    window: Window,
    experiment: Experiment,
    frameRate: float,
    syncSquares: Optional[SyncSquares],
    callback: Any = None,
    shouldTerminate: Any = checkForEsc,
):

    window.color = STIMULATION_BACKGROUND_COLOR

    # unroll the experiment if necessary - i.e. if experiment consists of a single stimulus
    # type but with multiple values for at least one parameter, we unroll into multiple stimuli
    experiment = unrollExperiment(experiment)

    # create stimuli objects from descriptions
    stimuli = list(
        map(
            lambda s: createStim(s, window, frameRate, experiment.screenSettings),
            experiment.stimuli,
        )
    )

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
    stop = False
    for stimulus in stimuli:
        stop = playStimulus(
            window, stimulus, frameRate, syncSquares, _callback, shouldTerminate,
        )
        if syncSquares:
            syncSquares.turn_off(0)
            window.flip()
        if stop:
            break

    # reset window colour
    window.color = DEFAULT_BACKGROUND_COLOR
    window.flip()
