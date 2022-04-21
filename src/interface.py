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
from src.textures import drumTexture


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

        # controls whether to close the interface
        self.quit = False

        # parameters
        self.stimulusType = "drifting grating"
        self.parameters = copy.deepcopy(DEFAULT_PARAMS)

        # create components to render
        self.syncSquares = SyncSquares(self.displayWindow, "sync-squares")
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
            StimulusPanel(self.controlWindow, [-123, 60], self.selectStimulusType),
            ParametersPanel(
                self.controlWindow,
                [-117, -67],
                self.setStimulusParameter,
                copy.deepcopy(self.parameters["stimulus"]),
            ),
            SyncPanel(
                self.controlWindow,
                [254, -67],
                self.setSyncParameter,
                copy.deepcopy(self.parameters["sync"]),
            ),
            self.syncSquares,
        ]

        # register components (assign them to the window)
        for i in range(len(self.components)):
            self.components[i].register()

    def selectStimulusType(self, x):
        self.stimulusType = x

    def setStimulusParameter(self, key: str, value: Any) -> None:
        self.parameters["stimulus"][key] = value

    def setSyncParameter(self, key: str, value: Any) -> None:
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
        else:
            self.displayWindow.close()
            self.displayWindow = self.controlWindow
            self.frameRate = self.displayWindow.getActualFrameRate()

    def onQuitClicked(self, mouse: event.Mouse, button: Button) -> None:
        self.quit = True

    def onStartClicked(self, mouse: event.Mouse, button: Button) -> None:
        print(self.parameters)

        # toggle play button
        playButtonIdx = self.getComponentIndexById("play-button")
        if playButtonIdx != -1:
            self.components[playButtonIdx].toggle()

        # run selected stimulus
        if self.stimulusType == "drifting grating":
            self.playDriftingGrating()
        elif self.stimulusType == "static grating":
            self.playStaticGrating()
        elif self.stimulusType == "movie":
            self.playMovie()

        # toggle play button
        self.components[playButtonIdx].toggle()

    def onClick(self) -> None:
        for component in self.components:
            if self.clickHandled:
                break
            elif component.contains(self.mouse) and hasattr(component, "onClick"):
                component.onClick(self.mouse, component)
                self.clickHandled = True

    def onKeyPress(self, keys) -> None:
        if "escape" in keys:
            self.quit = True
            return
        for key in keys:
            for component in self.components:
                if hasattr(component, "onKeyPress"):
                    component.onKeyPress(key)

    def draw(self) -> None:
        for component in self.components:
            component.draw()
        self.controlWindow.flip()

    def playDriftingGrating(self) -> None:
        texture = drumTexture(self.frameRate, self.parameters)
        grating(
            self.displayWindow,
            self.syncSquares,
            texture,
            self.frameRate,
            self.parameters,
        )

    def playStaticGrating(self) -> None:
        time.sleep(5)

    def playMovie(self) -> None:
        time.sleep(5)

    def run(self) -> None:
        self.quit = self.clickHandled = False
        while not self.quit:
            # render interface
            self.draw()

            # listen for click events
            if self.mouse.getPressed()[0]:
                self.onClick()
            else:
                self.clickHandled = False

            # listen for keypresses
            keys = event.getKeys()
            self.onKeyPress(keys)

