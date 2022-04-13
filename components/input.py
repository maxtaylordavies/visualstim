from typing import Any, List
from psychopy.visual import Window, TextBox2, circle, rect

from constants import DARKGREY, GREEN, RED, WHITE
from utils import noOp


class TextInput:
    def __init__(
        self, id: str, text: str, labelText: str, pos: List[int], onChange=noOp,
    ) -> None:
        self.id = id
        self.text = text
        self.labelText = labelText
        self.pos = pos
        self.onChange = onChange
        self.active = False

    def register(self, window, text="."):
        self.window = window
        self.input = TextBox2(
            window,
            text if text != "." else self.text,
            "Open Sans",
            units="pix",
            letterHeight=18,
            colorSpace="rgb255",
            color="black",
            fillColor=WHITE,
            borderColor=GREEN if self.active else WHITE,
            borderWidth=3,
            bold=True,
            padding=5,
            size=[None, None],
            pos=self.pos,
            editable=self.active,
        )
        self.label = TextBox2(
            window,
            f"{self.labelText}:",
            "Open Sans",
            units="pix",
            letterHeight=18,
            colorSpace="rgb255",
            color=DARKGREY,
            fillColor=WHITE,
            borderColor=GREEN if self.active else WHITE,
            borderWidth=3,
            bold=False,
            padding=5,
            size=[None, None],
            pos=self.pos,
        )
        self.label.pos[0] -= (self.label.size[0] + self.input.size[0]) / 2
        self.input.pos[0] -= self.label.padding + self.input.padding
        self.mask = rect.Rect(
            window,
            units="pix",
            colorSpace="rgb255",
            fillColor=WHITE,
            size=[
                self.input.borderWidth,
                self.input.size[1] - self.input.borderWidth + 1,
            ],
            pos=[self.input.pos[0] - (self.input.size[0] / 2), self.input.pos[1]],
        )

    def toggle(self):
        self.active = not self.active
        self.update()

    def draw(self):
        self.label.draw()
        self.input.draw()
        self.mask.draw()

    def update(self):
        self.register(self.window, text=self.input.text)
        self.draw()
        self.input.hasFocus = self.active

    def contains(self, x):
        return self.input.contains(x) or self.label.contains(x) or self.mask.contains(x)

    def onClick(self, args):
        self.toggle()

    def onKeyPress(self, key):
        if key == "return":
            self.input.deleteCaretLeft()
            self.toggle()
        else:
            self.update()
