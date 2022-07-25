from datetime import datetime
import itertools
import json
import pathlib
from typing import Any, Dict, List

from src.window import Window
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
from src.utils import checkForEsc, parseParams
from src.constants import (
    COLORS,
    TRACKBALL_LISTENER_ADDR,
    TRACKBALL_LISTENER_PORT,
)
from src.socket import UDPSocket


def str2Stim(s: str) -> Stimulus:
    return {
        "static grating": StaticGrating,
        "drift grating": DriftingGrating,
        "osc grating": OscillatingGrating,
        "movie": Movie,
        "sparse noise": SparseNoise,
        "checkerboard": Checkerboard,
    }[s]


def createStim(x: Dict, window: Window, screenSettings: Dict, **kwargs) -> Dict:
    return {
        "stimulus": str2Stim(x["name"])(
            window, stimParams=x["params"], screenParams=screenSettings, **kwargs
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


def loadExperiment(window: Window, filename: str) -> Experiment:
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
    socket: UDPSocket,
    _callback: Any = None,
    shouldTerminate: Any = checkForEsc,
    logGenerator=None,
):
    # unroll the experiment if necessary - i.e. if experiment consists of a single stimulus
    # type but with multiple values for at least one parameter, we unroll into multiple stimuli
    experiment = unrollExperiment(experiment)

    # create stimuli objects from descriptions
    stimuli, l = [], len(experiment.stimuli)
    for i in range(l):
        experiment.stimuli[i]["params"]["label"] = f"stimulus {i+1}/{l}"
        stimuli.append(
            createStim(
                experiment.stimuli[i],
                window,
                experiment.screenSettings,
                logGenerator=logGenerator,
            )
        )

    # if we want to monitor trackball, create a socket and
    # a lambda function for parsing stop signals sent over UDP
    if experiment.syncSettings["trackball"]:
        socket.sendData("start", TRACKBALL_LISTENER_ADDR, TRACKBALL_LISTENER_PORT)
        checkUDPCommand = lambda: socket.parseCommand()
    else:
        checkUDPCommand = lambda: ("", None)

    def callback(frameIdx: int):
        # check for switch or termination signal
        cmd, val = checkUDPCommand()
        if cmd or shouldTerminate():
            return (cmd or "stop", val)

        # send a sync pulse if needed
        if (
            experiment.syncSettings["sync"]
            and experiment.syncSettings["pulse length"]
            and frameIdx % experiment.syncSettings["sync interval"]
            in {0, experiment.syncSettings["pulse length"]}
        ):
            window.toggleSyncSquare(1)
        _callback()

    def _draw():
        window.flip()

    # clear the window for stimulus display
    window.clearComponents()
    window.setBackgroundColor(COLORS[experiment.screenSettings["background"]])
    window.flip()

    # trigger loop
    if experiment.syncSettings["sync"]:
        window.toggleSyncSquare(0)  # turn on trigger square
        for i in range(
            int(window.frameRate * experiment.syncSettings["trigger duration"])
        ):
            # execute per-frame callback
            callbackResult = callback(i)
            if callbackResult:
                cmd, _ = callbackResult
                if cmd == "stop":
                    break

            if i == experiment.syncSettings["pulse length"]:
                window.toggleSyncSquare(0)  # turn off trigger square

            _draw()

    # cycle through + display stimuli
    stimIdx, signal, experimentFrameIdx = 0, None, 0
    blankFrames = int(window.frameRate * experiment.screenSettings["blank"])
    while stimIdx < len(stimuli):
        # display the stimulus
        signal, experimentFrameIdx = playStimulus(
            window, stimuli[stimIdx], callback, experimentFrameIdx,
        )

        # make sure we don't leave the sync square on
        window.turnOffSyncSquare(1)
        window.flip()

        # interstimulus blank
        if signal == None:
            for i in range(experimentFrameIdx, experimentFrameIdx + blankFrames):
                callback(i)
                _draw()
            experimentFrameIdx += blankFrames
            window.turnOffSyncSquare(1)
            window.flip()

        stimIdx += 1

        # if we've recieved a signal to change stimulus or stop the experiment,
        # then process it accordingly
        if signal != None:
            cmd, val = signal
            if cmd == "stop":
                break
            elif cmd == "switch":
                stimIdx = int(val)

    # stop trackball listener if running
    if experiment.syncSettings["trackball"]:
        socket.sendData("stop", TRACKBALL_LISTENER_ADDR, TRACKBALL_LISTENER_PORT)

    # reset window
    window.setBackgroundColor(COLORS["white"])
    window.activateComponents()
    window.flip()
