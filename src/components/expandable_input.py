import numpy as np

from src.components.core import Box, Button, Component, Panel, Textbox
from .core.input import TextInput
from src.constants import COLORS
from src.utils import noOp


class ExpandableInput(Component):
    def __init__(
        self, *args, value: float, labelText: str, onChange=noOp, _type=None, **kwargs,
    ) -> None:
        super().__init__(*args, listenForKeyPresses=True, **kwargs)
        self.initialValue = self.start = self.stop = value
        self.steps = 1
        self.random = False
        self.labelText = labelText
        self.onChange = onChange
        self.active = False
        self.type = _type or type(value)

    def register(self):
        self.registerActive() if self.active else self.registerInactive()
        super().register()

    def registerInactive(self):
        text = str(self.start)
        if self.start != self.stop:
            text = "rand" if self.random else "multi"
        self.input = Textbox(
            self.window,
            f"{self.id}-input",
            pos=self.pos,
            text=text,
            bold=True,
            editable=self.active,
        )
        self.label = Textbox(
            self.window,
            f"{self.id}-label",
            pos=self.pos,
            text=self.labelText,
            color=COLORS["darkgrey"],
        )

        labelSize, inputSize = self.label.size, self.input.size
        self.label.setPos(
            [self.label.pos[0] - (labelSize[0] + inputSize[0]) / 2, self.label.pos[1]]
        )
        self.input.setPos(
            [
                self.input.pos[0] - self.label.padding + self.input.padding,
                self.input.pos[1],
            ]
        )

        if self.size != [None, None]:
            diffx = self.size[0] - self.getSize()[0] if self.size[0] else 0
            diffy = self.size[1] - self.getSize()[1] if self.size[1] else 0

            self.input.setSize([inputSize[0] + diffx, inputSize[1] + diffy])
            self.input.setPos([self.input.pos[0] + (diffx / 2), self.input.pos[1]])
            self.label.setSize([labelSize[0], labelSize[1] + diffy])

        left, right = self.edges()
        center = (left + right) / 2
        self.label.setPos([self.label.pos[0] + self.pos[0] - center, self.label.pos[1]])
        self.input.setPos([self.input.pos[0] + self.pos[0] - center, self.input.pos[1]])

        self.children = [
            Box(
                self.window,
                f"{self.id}-box",
                pos=[self.pos[0], self.pos[1] + 1],
                size=[right - left + 2, self.input.size[1] + 2],
                color=COLORS["white"],
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
            value=str(self.start),
            labelText="start",
            pos=labelPos,
            zIndex=20,
            fill=COLORS["lightgrey"],
            highlight=False,
            onChange=self.onStartChange,
            _type=self.type,
        )
        self.stopInput = TextInput(
            self.window,
            f"{self.id}-start-input",
            value=str(self.stop),
            labelText="stop",
            pos=labelPos,
            zIndex=20,
            fill=COLORS["lightgrey"],
            highlight=False,
            onChange=self.onStopChange,
            _type=self.type,
        )
        self.stepsInput = TextInput(
            self.window,
            f"{self.id}-start-input",
            value=str(self.steps),
            labelText="steps",
            pos=labelPos,
            zIndex=20,
            fill=COLORS["lightgrey"],
            highlight=False,
            onChange=self.onStepsChange,
            _type=int,
        )
        self.randomiseButton = Button(
            self.window,
            f"{self.id}-randomise-button",
            text=" random",
            color=COLORS["white"],
            fill=COLORS["green"] if self.random else COLORS["lightgrey"],
            pos=labelPos,
            size=[None, 32],
            onClick=lambda a, b: self.toggleRandom(),
        )

        self.children = [
            Box(
                self.window,
                f"{self.id}-box",
                pos=boxPos,
                size=[right - left + 2, self.input.size[1] + boxHeightDiff],
                color=COLORS["white"],
                borderColor=COLORS["green"],
                borderWidth=3,
                children=[
                    self.label,
                    Panel(
                        self.window,
                        f"{self.id}-panel",
                        labelText="",
                        pos=[boxPos[0] + 14, boxPos[1] - 16],
                        children=[
                            self.startInput,
                            self.stopInput,
                            self.stepsInput,
                            self.randomiseButton,
                        ],
                        rows=2,
                        padding=5,
                        fill=COLORS["transparent"],
                        listenForKeyPresses=True,
                    ),
                ],
                onClick=lambda a, b: self.toggle(),
                listenForKeyPresses=True,
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
        elif self.start == self.stop:
            self.steps = 1
        else:
            self.steps = max(self.steps, 2)
        self.register()

    def generateValues(self):
        if self.start == self.stop:
            return self.start
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
