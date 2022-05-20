from typing import Any, List

import numpy as np
from psychopy.visual import Window, TextBox2, rect

from src.components.core import Box, Button, Component, Panel
from .core.input import TextInput
from src.constants import DARKGREY, GREEN, LIGHTGREY, RED, WHITE, TRANSPARENT
from src.utils import noOp


class ExpandableInput(Component):
    def __init__(
        self,
        window: Window,
        id: str,
        value: float,
        labelText: str,
        pos: List[int],
        size=[None, None],
        onChange=noOp,
        zIndex=0,
    ) -> None:
        super().__init__(window, id, pos, size, zIndex)
        self.initialValue = self.start = self.stop = value
        self.steps = 1
        self.random = False
        self.labelText = labelText
        self.onChange = onChange
        self.active = False

    def register(self):
        self.registerActive() if self.active else self.registerInactive()
        super().register()

    def registerInactive(self):
        text = str(self.start)
        if self.start != self.stop:
            text = "rand" if self.random else "cycle"
        self.input = TextBox2(
            self.window,
            text,
            "Open Sans",
            units="pix",
            letterHeight=18,
            colorSpace="rgb255",
            color="black",
            fillColor=WHITE,
            bold=True,
            padding=5,
            size=[None, None],
            pos=self.pos,
            editable=self.active,
        )
        self.label = TextBox2(
            self.window,
            f"{self.labelText}",
            "Open Sans",
            units="pix",
            letterHeight=18,
            colorSpace="rgb255",
            color=DARKGREY,
            fillColor=WHITE,
            bold=False,
            padding=5,
            size=[None, None],
            pos=self.pos,
        )

        self.label.pos[0] -= (self.label.size[0] + self.input.size[0]) / 2
        self.input.pos[0] -= self.label.padding + self.input.padding

        if self.size != [None, None]:
            diffx = self.size[0] - self.getSize()[0] if self.size[0] else 0
            diffy = self.size[1] - self.getSize()[1] if self.size[1] else 0
            self.input.size = [self.input.size[0] + diffx, self.input.size[1] + diffy]
            self.input.pos = [self.input.pos[0] + (diffx / 2), self.input.pos[1]]
            self.label.size = [self.label.size[0], self.label.size[1] + diffy]

        left, right = self.edges()
        center = (left + right) / 2
        self.label.pos[0] += self.pos[0] - center
        self.input.pos[0] += self.pos[0] - center

        self.children = [
            Box(
                self.window,
                f"{self.id}-box",
                WHITE,
                [self.pos[0], self.pos[1] + 1],
                [right - left + 2, self.input.size[1] + 2],
                children=[self.label, self.input],
                onClick=lambda a, b: self.toggle(),
            )
        ]

    def registerActive(self):
        left, right = self.edges()

        boxHeightDiff = 116 - self.getSize()[1]
        boxPos = [self.pos[0], self.pos[1] - (boxHeightDiff / 2) + 1]
        labelPos = self.label.pos

        self.startInput = TextInput(
            self.window,
            f"{self.id}-start-input",
            str(self.start),
            "start",
            labelPos,
            zIndex=20,
            fill=LIGHTGREY,
            highlight=False,
            onChange=self.onStartChange,
        )
        self.stopInput = TextInput(
            self.window,
            f"{self.id}-start-input",
            str(self.stop),
            "stop",
            labelPos,
            zIndex=20,
            fill=LIGHTGREY,
            highlight=False,
            onChange=self.onStopChange,
        )
        self.stepsInput = TextInput(
            self.window,
            f"{self.id}-start-input",
            str(self.steps),
            "steps",
            labelPos,
            zIndex=20,
            fill=LIGHTGREY,
            highlight=False,
            onChange=self.onStepsChange,
        )
        self.randomiseButton = Button(
            self.window,
            "temp-button",
            " random",
            WHITE,
            GREEN if self.random else LIGHTGREY,
            labelPos,
            size=[None, 32],
            onClick=lambda a, b: self.toggleRandom(),
        )

        self.children = [
            Box(
                self.window,
                f"{self.id}-box",
                WHITE,
                boxPos,
                [right - left + 2, self.input.size[1] + boxHeightDiff],
                borderColor=GREEN,
                borderWidth=3,
                children=[
                    self.label,
                    Panel(
                        self.window,
                        f"{self.id}-panel",
                        "",
                        [boxPos[0], boxPos[1] - 16],
                        [
                            self.startInput,
                            self.stopInput,
                            self.stepsInput,
                            self.randomiseButton,
                        ],
                        rows=2,
                        padding=8,
                        background=TRANSPARENT,
                    ),
                ],
                onClick=lambda a, b: self.toggle(),
            )
        ]

    def onStartChange(self, x):
        self.start = float(x)
        self.afterChange()

    def onStopChange(self, x):
        self.stop = float(x)
        self.afterChange()

    def onStepsChange(self, x):
        self.steps = int(x)
        self.afterChange()

    def toggleRandom(self):
        self.random = not self.random
        self.register()

    def afterChange(self):
        if self.start > self.stop:
            self.start = self.stop
        if self.start == self.stop:
            self.steps = 1
            self.register()

    def generateValues(self):
        if self.start == self.stop:
            return [self.start]
        vals = np.linspace(self.start, self.stop, self.steps)
        if self.random:
            np.random.shuffle(vals)
        return list(vals)

    def toggle(self):
        if self.active:
            self.onChange(self.generateValues())
        self.active = not self.active
        self.register()
        self.draw()

    def edges(self):
        rightEdge = self.input.pos[0] + (self.input.size[0] / 2)
        leftEdge = self.label.pos[0] - (self.label.size[0] / 2)
        return [leftEdge, rightEdge]

    def getSize(self):
        leftEdge, rightEdge = self.edges()
        return [rightEdge - leftEdge, self.input.size[1]]

    def setSize(self, size):
        self.size = size
        self.register()
        self.draw()
