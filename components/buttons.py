from typing import Any, List
from psychopy.visual import Window, TextBox2, circle

from constants import GREEN, RED, WHITE
from utils import noOp


class Button:
    def __init__(
        self,
        id: str,
        text: str,
        color: List[int],
        fill: List[int],
        pos: List[int],
        padding=2,
        onClick=noOp,
    ) -> None:
        self.id = id
        self.text = text
        self.color = color
        self.fill = fill
        self.pos = pos
        self.padding = padding
        self.onClick = onClick

    def register(self, window):
        self.shape = TextBox2(
            window,
            f" {self.text} ",
            "Open Sans",
            units="pix",
            letterHeight=18,
            colorSpace="rgb255",
            color=self.color,
            fillColor=self.fill,
            bold=True,
            padding=self.padding,
            size=[None, None],
            pos=self.pos,
        )

    def changeFill(self, fill):
        print(f"changing fill to {fill}")
        self.fill = fill
        self.shape.fillColor = self.fill
        self.draw()

    def draw(self):
        self.shape.draw()

    def contains(self, x):
        return self.shape.contains(x)


class PlayButton:
    def __init__(self, id: str, radius: int, pos: List[int], onClick=noOp,) -> None:
        self.id = id
        self.radius = radius
        self.pos = pos
        self.onClick = onClick
        self.state = "play"

    def register(self, window):
        self.shapes = [
            circle.Circle(
                window,
                radius=self.radius,
                units="pix",
                colorSpace="rgb255",
                fillColor=GREEN,
                pos=self.pos,
            ),
            circle.Polygon(
                window,
                radius=self.radius / 1.7,
                fillColor=WHITE,
                units="pix",
                pos=self.pos,
                ori=90,
            ),
        ]

    def toggle(self):
        self.state = "stop" if self.state == "play" else "play"
        self.shapes[1].edges = 3 if self.state == "play" else 4
        self.shapes[1].ori = 90 if self.state == "play" else 45
        self.shapes[0].fillColor = GREEN if self.state == "play" else RED

    def draw(self):
        for shape in self.shapes:
            shape.draw()

    def contains(self, x):
        for shape in self.shapes:
            if shape.contains(x):
                return True
        return False
