import time

from psychopy import visual, event, core

from constants import WHITE, PURPLE, YELLOW, RED
from utils import checkForEsc, noOp
from components import Button, PlayButton, Box, Panel, StimulusPanel, ParametersPanel
from grating import grating
from textures import drumTexture


class Interface:
    def __init__(self, fullscreen=False):
        self.screenNum = 0
        self.fullscreen = fullscreen
        self.controlWindow = visual.Window(
            screen=self.screenNum, fullscr=self.fullscreen, units="pix", color=WHITE,
        )
        self.displayWindow = self.controlWindow
        self.frameRate = self.displayWindow.getActualFrameRate()
        self.mouse = event.Mouse(visible=True, win=self.controlWindow)
        self.stimulusType = "drifting grating"
        self.quit = False

        def onStimulusTypeSelected(stimulusType):
            self.stimulusType = stimulusType

        self.components = [
            Button("logo-button", "visualstim v0.1", PURPLE, WHITE, [-320, 273]),
            PlayButton("play-button", 16, [125, 270], self.onStartClicked),
            Button(
                "switch-screen-button",
                "switch screen",
                WHITE,
                YELLOW,
                [215, 270],
                onClick=self.onSwitchScreenClicked,
            ),
            Button(
                "quit-button",
                "quit (esc)",
                WHITE,
                RED,
                [340, 270],
                onClick=self.onQuitClicked,
            ),
            StimulusPanel([0, 100], onStimulusTypeSelected),
            ParametersPanel([0, -50], noOp),
        ]
        for i in range(len(self.components)):
            self.components[i].register(self.controlWindow)

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
            )
            self.frameRate = 30
        else:
            self.displayWindow.close()
            self.displayWindow = self.controlWindow
            self.frameRate = self.displayWindow.getActualFrameRate()

    def onQuitClicked(self, mouse: event.Mouse):
        self.quit = True

    def onStartClicked(self, mouse: event.Mouse):
        # toggle play button
        playButtonIdx = self.getComponentIndexById("play-button")
        if playButtonIdx != -1:
            self.components[playButtonIdx].toggle()

        # run selected stimulus
        if self.stimulusType == "drifting grating":
            self.playDriftingGrating()
        # elif self.stimulusType == "static grating":
        #     self.playStaticGrating()
        # elif self.stimulusType == "movie":
        #     self.playMovie()

        # toggle play button
        # self.components[playButtonIdx].toggle()

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
        grating(self.displayWindow, texture, 10, self.frameRate)

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

