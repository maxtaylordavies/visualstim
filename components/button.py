from typing import Any, List
from psychopy.visual import Window, TextBox2


def noOp(args):
    return


class Button:
    def __init__(
        self, text: str, color: List[int], fill: List[int], pos: List[int], onClick=noOp
    ) -> None:
        self.text = text
        self.color = color
        self.fill = fill
        self.pos = pos
        self.onClick = onClick

    def register(self, window):
        self.shape = TextBox2(
            window,
            f" {self.text} ",
            "Open Sans",
            units="pix",
            letterHeight=20,
            colorSpace="rgb255",
            color=self.color,
            fillColor=self.fill,
            bold=True,
            padding=2,
            size=[None, None],
            pos=self.pos,
        )

    def draw(self):
        self.shape.draw()

    def contains(self, x):
        return self.shape.contains(x)
