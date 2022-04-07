from typing import Any, List
from psychopy.visual import Window, TextBox2, circle


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


class PlayButton:
    def __init__(self, radius: int, pos: List[int], onClick=noOp,) -> None:
        self.radius = radius
        self.pos = pos
        self.onClick = onClick

    def register(self, window):
        self.shapes = [
            circle.Circle(
                window,
                radius=self.radius,
                units="pix",
                colorSpace="rgb255",
                fillColor=[0, 199, 129],
                pos=self.pos,
            ),
            circle.Polygon(
                window, radius=20, fillColor="white", units="pix", pos=self.pos, ori=90
            ),
        ]

    def draw(self):
        for shape in self.shapes:
            shape.draw()

    def contains(self, x):
        for shape in self.shapes:
            if shape.contains(x):
                return True
        return False
