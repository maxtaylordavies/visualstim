import time

from psychopy import visual, event, core

from constants import WHITE, PURPLE, YELLOW, RED
from utils import checkForEsc, noOp
from components import (
    Button,
    PlayButton,
    Box,
    StimulusPanel,
    ParametersPanel,
    SyncSquares,
)
from grating import grating
from textures import drumTexture


class Interface:
    def __init__(self, fullscreen=False):
        self.screenNum = 0
        self.fullscreen = fullscreen
        self.controlWindow = visual.Window(
            screen=self.screenNum,
            fullscr=self.fullscreen,
            units="pix",
            color=WHITE,
            colorSpace="rgb255",
        )
        self.displayWindow = self.controlWindow
        self.frameRate = self.displayWindow.getActualFrameRate()
        self.mouse = event.Mouse(visible=True, win=self.controlWindow)
        self.quit = False

        self.parameters = {
            "stimulus type": "drifting grating",
            "spatial frequency": 10,
            "temporal frequency": 10,
            "trigger duration": 5,
            "stim duration": 10,
        }

        def onStimulusTypeSelected(stimulusType):
            self.stimulusType = stimulusType

        self.syncSquares = SyncSquares(self.displayWindow, "sync-squares")

        self.components = [
            Button(
                self.controlWindow,
                "logo-button",
                "visualstim v0.1",
                PURPLE,
                WHITE,
                [-320, 273],
            ),
            PlayButton(
                self.controlWindow, "play-button", 16, [125, 270], self.onStartClicked
            ),
            Button(
                self.controlWindow,
                "switch-screen-button",
                "switch screen",
                WHITE,
                YELLOW,
                [215, 270],
                onClick=self.onSwitchScreenClicked,
            ),
            Button(
                self.controlWindow,
                "quit-button",
                "quit (esc)",
                WHITE,
                RED,
                [340, 270],
                onClick=self.onQuitClicked,
            ),
            StimulusPanel(
                self.controlWindow,
                [0, 100],
                lambda x: self.setParameter("stimulus type", x),
            ),
            ParametersPanel(self.controlWindow, [0, -50], self.setParameter),
            self.syncSquares,
        ]

        for i in range(len(self.components)):
            self.components[i].register()

    def setParameter(self, key, value):
        self.parameters[key] = value

    def getComponentIndexById(self, id: str):
        for i, c in enumerate(self.components):
            if c.id == id:
                return i
        return -1

    def onSwitchScreenClicked(self, mouse: event.Mouse):
        self.screenNum = 1 - self.screenNum
        if self.screenNum:
            self.displayWindow = visual.Window(
                screen=self.screenNum,
                fullscr=self.fullscreen,
                units="pix",
                color=[255, 255, 255],
                colorSpace="rgb255"
            )
            self.frameRate = 30
        else:
            self.displayWindow.close()
            self.displayWindow = self.controlWindow
            self.frameRate = self.displayWindow.getActualFrameRate()

    def onQuitClicked(self, mouse: event.Mouse):
        self.quit = True

    def onStartClicked(self, mouse: event.Mouse):
        print(self.parameters)

        # toggle play button
        playButtonIdx = self.getComponentIndexById("play-button")
        if playButtonIdx != -1:
            self.components[playButtonIdx].toggle()

        # run selected stimulus
        if self.parameters["stimulus type"] == "drifting grating":
            self.playDriftingGrating()
        elif self.stimulusType == "static grating":
            self.playStaticGrating()
        elif self.stimulusType == "movie":
            self.playMovie()

        # toggle play button
        self.components[playButtonIdx].toggle()

    def onClick(self):
        for component in self.components:
            if self.clickHandled:
                break
            elif component.contains(self.mouse) and hasattr(component, "onClick"):
                component.onClick(self.mouse)
                self.clickHandled = True

    def onKeyPress(self, keys):
        if "escape" in keys:
            self.quit = True
            return
        for key in keys:
            for component in self.components:
                if hasattr(component, "onKeyPress"):
                    component.onKeyPress(key)

    def draw(self):
        for component in self.components:
            component.draw()
        self.controlWindow.flip()

    def playDriftingGrating(self):
        texture = drumTexture(self.frameRate)
        grating(
            self.displayWindow,
            self.syncSquares,
            texture,
            [self.parameters["trigger duration"], self.parameters["stim duration"]],
            self.frameRate,
        )

    def playStaticGrating(self):
        time.sleep(5)

    def playMovie(self):
        time.sleep(5)

    def run(self):
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

