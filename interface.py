from psychopy import visual, event

from utils import checkForEsc
from components import Button, PlayButton, Box, Panel, StimulusPanel
from grating import grating
from textures import drumTexture


class Interface:
    def __init__(self, components, fullscreen=False):
        self.screenNum = 0
        self.fullscreen = fullscreen
        self.controlWindow = visual.Window(
            screen=self.screenNum,
            fullscr=self.fullscreen,
            units="pix",
            color=[255, 255, 255],
        )
        self.displayWindow = self.controlWindow
        self.frameRate = self.displayWindow.getActualFrameRate()
        self.mouse = event.Mouse(visible=True, win=self.controlWindow)
        self.quit = False
        self.stimulusType = "drum grating"

        def onStimulusTypeSelected(stimulusType):
            self.stimulusType = stimulusType
            print(self.stimulusType)

        self.components = components + [
            Button(
                "logo-button", "visualstim v0.1", [125, 76, 219], "white", [-320, 273]
            ),
            PlayButton("play-button", 16, [125, 270], self.onStartClicked),
            Button(
                "switch-screen-button",
                "switch screen",
                "white",
                [255, 170, 21],
                [215, 270],
                onClick=self.onSwitchScreenClicked,
            ),
            Button(
                "quit-button",
                "quit (esc)",
                "white",
                [255, 64, 64],
                [340, 270],
                onClick=self.onQuitClicked,
            ),
            StimulusPanel([0, 0], onStimulusTypeSelected),
        ]
        for i in range(len(self.components)):
            self.components[i].register(self.controlWindow)

    def getComponentIndexById(self, id: str):
        for i, c in enumerate(self.components):
            if c.id == id:
                return i
        return -1

    def onSwitchScreenClicked(self):
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

    def onStartClicked(self):
        playButtonIdx = self.getComponentIndexById("play-button")
        if playButtonIdx != -1:
            self.components[playButtonIdx].toggle()
        texture = drumTexture(self.frameRate)
        grating(self.displayWindow, texture, 10, self.frameRate)
        self.components[playButtonIdx].toggle()

    def onQuitClicked(self):
        self.quit = True

    def run(self):
        clickHandled = False
        while not self.quit:
            # draw components onto screen
            for component in self.components:
                component.draw()
            self.controlWindow.flip()

            # listen for click events within components
            if self.mouse.getPressed()[0]:
                for component in self.components:
                    if (
                        clickHandled
                        or isinstance(component, Box)
                        or not component.contains(self.mouse)
                    ):
                        continue
                    elif isinstance(component, (Panel, StimulusPanel)):
                        component.handleClick(self.mouse)
                    else:
                        component.onClick()
                    clickHandled = True
            else:
                clickHandled = False

            # exit if user has pressed esc
            if checkForEsc():
                self.quit = True
