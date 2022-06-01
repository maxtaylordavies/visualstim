from typing import Any, List
from psychopy.visual import Window, TextBox2, rect

from src.components.core import Component
from src.constants import DARKGREY, GREEN, RED, WHITE
from src.utils import noOp


class TextInput(Component):
    def __init__(
        self,
        window: Window,
        id: str,
        value: Any,
        labelText: str,
        pos: List[int],
        size=[None, None],
        onChange=noOp,
        zIndex=0,
        fill=WHITE,
        highlight=True,
    ) -> None:
        super().__init__(window, id, pos, size, zIndex)
        self.initialValue = self.value = value
        self.labelText = labelText
        self.onChange = onChange
        self.active = False
        self.fill = fill
        self.highlight = highlight

    def register(self, text="$"):
        self.input = TextBox2(
            self.window,
            text if text != "$" else str(self.value),
            "Open Sans",
            units="pix",
            letterHeight=18,
            colorSpace="rgb255",
            color="black",
            fillColor=self.fill,
            borderColor=GREEN if (self.active and self.highlight) else WHITE,
            borderWidth=3,
            bold=True,
            padding=5,
            size=[None, None],
            pos=self.pos,
            editable=self.active,
        )
        self.label = TextBox2(
            self.window,
            self.labelText,
            "Open Sans",
            units="pix",
            letterHeight=18,
            colorSpace="rgb255",
            color=DARKGREY,
            fillColor=self.fill,
            borderColor=GREEN if (self.active and self.highlight) else WHITE,
            borderWidth=3,
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
            self.input.text = (
                self.input.text if self.input.text else str(self.initialValue)
            )
            self.value = type(self.initialValue)(self.input.text)
            self.onChange(self.value)
        self.active = not self.active
        self.update()

    def update(self):
        self.register(text=self.input.text)
        self.draw()
        self.input.hasFocus = self.active

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
            self.input.deleteCaretLeft()
            self.toggle()
        else:
            self.update()
