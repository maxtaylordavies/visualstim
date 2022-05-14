import copy
from typing import Any, List

from psychopy import visual, event

from src.constants import (
    DEFAULT_PARAMS,
    STIMULUS_PARAMETER_MAP,
    WHITE,
    PURPLE,
    YELLOW,
    RED,
)
from src.components.core import Button, Component, PlayButton
from src.components import (
    ModeSelector,
    StimulusPanel,
    ParametersPanel,
    SyncPanel,
    SyncSquares,
    ScriptSelector,
)
from src.stimuli import Stimulus, DriftingGrating, StaticGrating, Movie
from src.utils import checkForEsc
from src.experiments import (
    str2Stim,
    Experiment,
    playExperiment,
    loadExperiment as _loadExperiment,
)


class Interface:
    def __init__(self, fullscreen=False):
        # start in interactive mode by default
        self.mode = "interactive"

        # create window
        self.screenNum = 0
        self.fullscreen = fullscreen
        self.controlWindow = visual.Window(
            size=[900, 600],
            screen=self.screenNum,
            fullscr=self.fullscreen,
            units="pix",
            color=WHITE,
            colorSpace="rgb255",
        )
        self.displayWindow = self.controlWindow
        self.frameRate = self.displayWindow.getActualFrameRate() or 30
        self.syncSquares = None

        # create mouse object to listen for click events
        self.mouse = event.Mouse(visible=True, win=self.controlWindow)
        self.clickHandled = False

        # controls whether to close the interface
        self.quit = False

        # flag for whether we're currently showing stimulus
        self.playing = False

        # load default experiment
        self.loadExperiment("default.json")

        # create components to render
        # (and register them)
        self.createComponents()

    def createComponents(self) -> None:
        self.components = [
            Button(
                self.controlWindow,
                "logo-button",
                "visualstim v0.1",
                PURPLE,
                WHITE,
                [-370, 273],
            ),
            ModeSelector(
                self.controlWindow,
                "mode-selector",
                [-200, 273],
                self.mode,
                self.toggleMode,
            ),
            PlayButton(
                self.controlWindow, "play-button", 16, [175, 270], self.onStartClicked
            ),
            Button(
                self.controlWindow,
                "switch-screen-button",
                "switch screen",
                WHITE,
                YELLOW,
                [265, 270],
                onClick=self.onSwitchScreenClicked,
            ),
            Button(
                self.controlWindow,
                "quit-button",
                "quit (esc)",
                WHITE,
                RED,
                [390, 270],
                onClick=self.onQuitClicked,
            ),
        ] + (
            self.scriptingModeComponents()
            if self.mode == "scripting"
            else self.interactiveModeComponents()
        )
        # register components (assign them to the window)
        for i in range(len(self.components)):
            self.components[i].register()

    def interactiveModeComponents(self) -> List[Component]:
        return [
            StimulusPanel(
                self.controlWindow,
                "stimulus-panel",
                [-123, 60],
                self.selectStimulusType,
            ),
            ParametersPanel(
                self.controlWindow,
                "stim-params-panel",
                [-117, -67],
                self.setStimulusParameter,
                self.filterStimulusParams(),
            ),
            SyncPanel(
                self.controlWindow,
                "sync-params-panel",
                [256, -15],
                self.setSyncParameter,
                copy.deepcopy(self.experiment.syncSettings),
            ),
        ]

    def scriptingModeComponents(self) -> List[Component]:
        return [
            ScriptSelector(
                self.controlWindow, "script-selector", [0, 0], self.loadExperiment
            )
        ]

    def toggleMode(self) -> None:
        self.mode = ("interactive", "scripting")[self.mode == "interactive"]
        self.loadExperiment("default.json")
        self.createComponents()

    def loadExperiment(self, filename):
        self.experiment = _loadExperiment(self.displayWindow, self.frameRate, filename)
        if self.experiment.syncSettings["sync"]:
            self.createSyncSquares()
        elif self.syncSquares:
            self.removeSyncSquares()

    def filterStimulusParams(self):
        return {
            k: v
            for k, v in self.experiment.stimuli[0]["params"].items()
            if k in STIMULUS_PARAMETER_MAP[self.experiment.stimuli[0]["name"]]
        }

    def createSyncSquares(self):
        self.syncSquares = SyncSquares(self.displayWindow, "sync-squares")
        self.components = [c for c in self.components if c.id != "sync-squares"]
        self.components.append(self.syncSquares)
        self.components[-1].register()

    def removeSyncSquares(self):
        self.syncSquares = None
        self.components = [c for c in self.components if c.id != "sync-squares"]

    def selectStimulusType(self, x):
        # set stimulus type
        self.experiment.stimuli[0]["name"] = x

        # update the parameters shown in the params panel
        paramsPanelIdx = self.getComponentIndexById("stim-params-panel")
        if paramsPanelIdx != -1:
            self.components[paramsPanelIdx].resetParams(self.filterStimulusParams())

    def setStimulusParameter(self, key: str, value: Any) -> None:
        self.experiment.stimuli[0]["params"][key] = value

    def setSyncParameter(self, key: str, value: Any) -> None:
        if key == "sync":
            self.createSyncSquares() if value else self.removeSyncSquares()
        self.experiment.syncSettings[key] = value

    def getComponentIndexById(self, id: str) -> int:
        for i, c in enumerate(self.components):
            if c.id == id:
                return i
        return -1

    def onSwitchScreenClicked(self, mouse: event.Mouse, button: Button) -> None:
        self.screenNum = 1 - self.screenNum
        if self.screenNum:
            self.displayWindow = visual.Window(
                screen=self.screenNum,
                fullscr=self.fullscreen,
                units="pix",
                color=[255, 255, 255],
                colorSpace="rgb255",
            )
            self.frameRate = 30
            if self.experiment.syncSettings["sync"]:
                self.createSyncSquares()
            self.draw()
        else:
            self.displayWindow.close()
            self.displayWindow = self.controlWindow
            self.frameRate = self.displayWindow.getActualFrameRate()

    def onQuitClicked(self, mouse: event.Mouse, button: Button) -> None:
        self.quit = True

    def onStartClicked(self, mouse: event.Mouse, button: Button) -> None:
        playButtonIdx = self.getComponentIndexById("play-button")
        if playButtonIdx == -1:
            return

        # toggle play button
        self.playing = not self.playing
        self.components[playButtonIdx].toggle()
        self.draw()

        # if now in "playing" state, run the selected stimulus
        if self.playing:
            playExperiment(
                self.displayWindow,
                self.experiment,
                self.frameRate,
                self.syncSquares,
                callback=self.handleInput,
                shouldTerminate=self.shouldTerminateStimulation,
            )

            # if the stimulation hasn't been stopped prematurely by the user,
            # then we need to toggle the playing state + button
            if self.playing:
                self.components[playButtonIdx].toggle()
                self.draw()
                self.playing = not self.playing

    def onClick(self) -> None:
        for component in self.components:
            if component.contains(self.mouse) and hasattr(component, "onClick"):
                component.onClick(self.mouse, component)
                break

    def onKeyPress(self, keys) -> None:
        if "escape" in keys:
            self.quit = True
            return
        for key in keys:
            for component in self.components:
                if hasattr(component, "onKeyPress"):
                    component.onKeyPress(key)

    def handleInput(self) -> None:
        # listen for click events
        if self.mouse.getPressed()[0]:
            if not self.clickHandled:
                self.clickHandled = True
                self.onClick()
        else:
            self.clickHandled = False

        # listen for keypresses
        keys = event.getKeys()
        self.onKeyPress(keys)

    def draw(self) -> None:
        for component in self.components:
            component.draw()
        self.controlWindow.flip()
        if self.screenNum:
            self.displayWindow.flip()

    def shouldTerminateStimulation(self) -> bool:
        return checkForEsc() or (not self.playing) or (self.quit)

    def run(self) -> None:
        self.quit = self.clickHandled = False
        while not self.quit:
            # render interface
            self.draw()

            # listen for + handle user input
            self.handleInput()

    def start(self) -> None:
        self.run()

