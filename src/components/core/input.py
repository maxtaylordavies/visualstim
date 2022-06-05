from typing import Any, List
from psychopy.visual import Window, rect

from src.components.core import Component, Textbox
from src.constants import DARKGREY, GREEN, RED, WHITE
from src.utils import noOp, log


class TextInput(Component):
    def __init__(
        self,
        window: Window,
        id: str,
        value: Any,
        labelText: str,
        pos: List[int],
        onChange=noOp,
        fill=WHITE,
        highlight=True,
        **kwargs,
    ) -> None:
        super().__init__(window, id, pos, **kwargs)
        self.initialValue = self.value = value
        self.labelText = labelText
        self.onChange = onChange
        self.fill = fill
        self.highlight = highlight
        self.active = False

    def register(self, text="$"):
        self.input = Textbox(
            self.window,
            f"{self.id}-input",
            self.pos,
            text if text != "$" else str(self.value),
            fill=self.fill,
            borderColor=GREEN if (self.active and self.highlight) else WHITE,
            borderWidth=3,
            bold=True,
            editable=self.active,
        )

        self.label = Textbox(
            self.window,
            f"{self.id}-label",
            self.pos,
            self.labelText,
            color=DARKGREY,
            fill=self.fill,
            borderColor=GREEN if (self.active and self.highlight) else WHITE,
            borderWidth=3,
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

        self.mask = rect.Rect(
            self.window,
            units="pix",
            colorSpace="rgb255",
            fillColor=self.fill,
            size=[
                self.input.borderWidth,
                self.input.size[1] - self.input.borderWidth + 1,
            ],
            pos=[self.input.pos[0] - (self.input.size[0] / 2), self.input.pos[1]],
        )
        self.children = [self.label, self.input, self.mask]

    def toggle(self):
        if self.active:
            self.input.setText(
                self.input.getText() if self.input.getText() else str(self.initialValue)
            )
            self.value = type(self.initialValue)(self.input.getText())
            self.onChange(self.value)
        self.active = not self.active
        self.update()

    def update(self):
        self.register(text=self.input.getText())
        self.input.toggleFocus()
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
        self.update()

    def onClick(self, *args):
        self.toggle()

    def onKeyPress(self, key):
        if not self.active:
            return
        if key == "return":
            self.input.deleteCaret()
            self.toggle()
        else:
            self.update()
