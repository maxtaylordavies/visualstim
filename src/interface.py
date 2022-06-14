import copy
from typing import Any

from psychopy import event

from src.window import Window
from src.constants import STIMULUS_PARAMETER_MAP
from src.components.core import Button, Component
from src.components import (
    StimulusPanel,
    ParametersPanel,
    SyncPanel,
    ScreenPanel,
    SyncSquares,
    ScriptSelector,
    HeaderBar,
)
from src.utils import checkForEsc, log, getScreenResolution
from src.experiments import (
    playExperiment,
    loadExperiment as _loadExperiment,
    saveExperiment as saveExperiment,
)


class Interface(Component):
    def __init__(self, fullscreen=False):
        self.id = "root"

        # start in interactive mode by default
        self.mode = "interactive"

        # create window
        self.screenNum = 0
        self.fullscreen = fullscreen
        self.controlWindow = Window(fullscreen=self.fullscreen)
        self.displayWindow = self.controlWindow
        self.children = []
        self.syncSquares = None

        # create mouse object to listen for click events
        self.mouse = event.Mouse(visible=True, win=self.controlWindow)
        self.clickHandled = False

        # controls whether to close the interface
        self.quit = False

        # flag for whether we're currently playing and experiment
        self.playing = False

        # load default experiment
        self.loadExperiment("default.json")

        # get screen resolution and update screen params if necessary
        self.setResolution()

        # create + register children
        self.register()

    def register(self) -> None:
        self.children = [
            HeaderBar(
                self.controlWindow,
                "headerbar",
                mode=self.mode,
                toggleModeCallback=self.toggleMode,
                onStartClicked=self.onStartClicked,
                onSaveClicked=self.saveParameters,
                onSwitchScreenClicked=self.onSwitchScreenClicked,
                onQuitClicked=self.onQuitClicked,
            ),
            StimulusPanel(
                self.controlWindow,
                "stimulus-panel",
                pos=[-145, 120],
                callback=self.selectStimulusType,
            ),
            ParametersPanel(
                self.controlWindow,
                "stim-params-panel",
                pos=[-155, -20],
                callback=self.setStimulusParameter,
                initialParams=self.filterStimulusParams(),
            ),
            SyncPanel(
                self.controlWindow,
                "sync-params-panel",
                pos=[256, 60],
                callback=self.setSyncParameter,
                initialParams=copy.deepcopy(self.experiment.syncSettings),
            ),
            ScreenPanel(
                self.controlWindow,
                "screen-params-panel",
                pos=[-110, -170],
                callback=self.setScreenParameter,
                initialParams=copy.deepcopy(self.experiment.screenSettings),
            ),
            ScriptSelector(
                self.controlWindow,
                "script-selector",
                pos=[0, 0],
                callback=self.loadExperiment,
                hide=True,
            ),
        ]

        # register children (assign them to the window)
        super().register()
        self.controlWindow.assignComponents(self.children, activate=True)

    def setResolution(self) -> None:
        hor, ver = getScreenResolution(self.screenNum)
        self.setScreenParameter("h res", hor)
        self.setScreenParameter("v res", ver)

    def toggleMode(self) -> None:
        # set self.mode
        self.mode = ("interactive", "scripting")[self.mode == "interactive"]

        # load default experiment
        self.loadExperiment("default.json")

        # update UI
        for i, c in enumerate(self.children):
            if c.id != "headerbar":
                self.children[i].toggleHidden()

    def saveParameters(self):
        saveExperiment(self.experiment)

    def loadExperiment(self, filename):
        self.experiment = _loadExperiment(self.displayWindow, filename)
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
        self.children = [c for c in self.children if c.id != "sync-squares"]
        self.children.append(self.syncSquares)
        self.children[-1].register()

    def removeSyncSquares(self):
        self.syncSquares = None
        self.children = [c for c in self.children if c.id != "sync-squares"]

    def selectStimulusType(self, x):
        # set stimulus type
        self.experiment.stimuli[0]["name"] = x
        # update the parameters shown in the params panel
        paramsPanel = self.getComponentById("stim-params-panel")
        if paramsPanel:
            paramsPanel.resetParams(self.filterStimulusParams())
        self.afterParameterChange()

    def setStimulusParameter(self, key: str, value: Any) -> None:
        self.experiment.stimuli[0]["params"][key] = value
        self.afterParameterChange()

    def setSyncParameter(self, key: str, value: Any) -> None:
        if key == "sync":
            self.createSyncSquares() if value else self.removeSyncSquares()
            self.displayWindow.assignComponents(self.children, activate=True)
        self.experiment.syncSettings[key] = value
        self.afterParameterChange()

    def setScreenParameter(self, key: str, value: Any) -> None:
        print(key, value)
        self.experiment.screenSettings[key] = value
        self.afterParameterChange()

    def afterParameterChange(self):
        saveButton = self.getComponentById("save-button")
        if saveButton:
            saveButton.setUnsaved()

    def onSwitchScreenClicked(self, mouse: event.Mouse, button: Button) -> None:
        self.screenNum = 1 - self.screenNum
        if self.screenNum:
            self.displayWindow = Window(
                screenNum=self.screenNum, fullscreen=self.fullscreen
            )
            if self.experiment.syncSettings["sync"]:
                self.createSyncSquares()
            self.draw()
        else:
            self.displayWindow.close()
            self.displayWindow = self.controlWindow

    def onQuitClicked(self, mouse: event.Mouse, button: Button) -> None:
        self.quit = True

    def onStartClicked(self, mouse: event.Mouse, button: Button) -> None:
        playButton = self.getComponentById("play-button")
        if not playButton:
            return

        # toggle play button
        self.playing = not self.playing
        # self.children[playButtonIdx].toggle()
        playButton.toggle()
        self.draw()

        # if now in "playing" state, run the selected stimulus
        if self.playing:
            playExperiment(
                self.displayWindow,
                self.experiment,
                self.syncSquares,
                callback=self.handleInput,
                shouldTerminate=self.shouldTerminateStimulation,
            )

            # if the stimulation hasn't been stopped prematurely by the user,
            # then we need to toggle the playing state + button
            if self.playing:
                # self.children[playButtonIdx].toggle()
                playButton.toggle()
                self.draw()
                self.playing = not self.playing

    def onClick(self) -> None:
        for component in self.children:
            if component.contains(self.mouse) and hasattr(component, "onClick"):
                component.onClick(self.mouse, component)
                break

    def onKeyPress(self, keys) -> None:
        if "escape" in keys:
            self.quit = True
            return
        for key in keys:
            for component in self.children:
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
        # for component in self.children:
        #     component.draw()
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

