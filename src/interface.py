import copy
import time
from typing import Any

from psychopy import visual, event

from src.constants import DEFAULT_PARAMS, WHITE, PURPLE, YELLOW, RED
from src.components.core import Button, PlayButton
from src.components import (
    StimulusPanel,
    ParametersPanel,
    SyncPanel,
    SyncSquares,
)
from src.grating import grating
from src.movie import movie
from src.textures import drumTexture
from src.utils import checkForEsc


class Interface:
    def __init__(self, fullscreen=False):
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
        self.frameRate = self.displayWindow.getActualFrameRate()

        # create mouse object to listen for click events
        self.mouse = event.Mouse(visible=True, win=self.controlWindow)
        self.clickHandled = False

        # controls whether to close the interface
        self.quit = False

        # flag for whether we're currently showing stimulus
        self.playing = False

        # parameters
        self.stimulusType = "drifting grating"
        self.parameters = copy.deepcopy(DEFAULT_PARAMS)

        # create components to render
        self.components = [
            Button(
                self.controlWindow,
                "logo-button",
                "visualstim v0.1",
                PURPLE,
                WHITE,
                [-370, 273],
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
                copy.deepcopy(self.parameters["stimulus"]),
            ),
            SyncPanel(
                self.controlWindow,
                "sync-params-panel",
                [254, 10],
                self.setSyncParameter,
                copy.deepcopy(self.parameters["sync"]),
            ),
        ]

        # register components (assign them to the window)
        for i in range(len(self.components)):
            self.components[i].register()

        # create sync squares
        self.syncSquares = None
        if self.parameters["sync"]["sync status"]:
            self.createSyncSquares()

    def createSyncSquares(self):
        self.syncSquares = SyncSquares(self.displayWindow, "sync-squares")
        self.components = [c for c in self.components if c.id != "sync-squares"]
        self.components.append(self.syncSquares)
        self.components[-1].register()

    def removeSyncSquares(self):
        self.syncSquares = None
        self.components = [c for c in self.components if c.id != "sync-squares"]

    def selectStimulusType(self, x):
        self.stimulusType = x
        if x == "static grating":
            self.setStimulusParameter("temporal frequency", self.frameRate)
        else:
            self.setStimulusParameter(
                "temporal frequency", DEFAULT_PARAMS["stimulus"]["temporal frequency"]
            )

    def setStimulusParameter(self, key: str, value: Any) -> None:
        self.parameters["stimulus"][key] = value

    def setSyncParameter(self, key: str, value: Any) -> None:
        if key == "sync status":
            self.createSyncSquares() if value else self.removeSyncSquares()
        self.parameters["sync"][key] = value

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
            if self.parameters["sync"]["sync status"]:
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
            if "grating" in self.stimulusType:
                self.playGrating()
            elif self.stimulusType == "movie":
                self.playMovie()

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

    def handle_input(self) -> None:
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

    def playGrating(self) -> None:
        texture = drumTexture(self.frameRate, self.parameters)
        grating(
            self.displayWindow,
            self.syncSquares,
            texture,
            self.frameRate,
            params=self.parameters,
            callback=self.handle_input,
            shouldTerminate=self.shouldTerminateStimulation,
        )

    def playMovie(self) -> None:
        movie(
            self.displayWindow,
            "/Users/max/Documents/test.mp4",
            self.syncSquares,
            self.frameRate,
            params=self.parameters,
            callback=self.handle_input,
            shouldTerminate=self.shouldTerminateStimulation,
        )

    def run(self) -> None:
        self.quit = self.clickHandled = False
        while not self.quit:
            # render interface
            self.draw()

            # listen for + handle user input
            self.handle_input()

    def start(self) -> None:
        self.run()

