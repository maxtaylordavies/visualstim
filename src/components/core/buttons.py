from typing import Any, List
from psychopy.visual import Window, TextBox2, circle

from src.components.core import Component
from src.constants import GREEN, RED, WHITE, BLACK
from src.utils import noOp


class Button(Component):
    def __init__(
        self,
        window: Window,
        id: str,
        text: str,
        color: List[int],
        fill: List[int],
        pos: List[int],
        size=[None, None],
        bold=True,
        padding=2,
        onClick=None,
    ) -> None:
        super().__init__(window, id, pos, size, onClick=onClick)
        self.text = text
        self.color = color
        self.fill = fill
        self.bold = bold
        self.padding = padding
        self.borderWidth = 0

    def register(self):
        self.children = [
            TextBox2(
                self.window,
                f" {self.text} ",
                "Open Sans",
                alignment="center",
                units="pix",
                letterHeight=18,
                colorSpace="rgb255",
                color=self.color,
                fillColor=self.fill,
                bold=self.bold,
                padding=self.padding,
                size=self.size,
                pos=self.pos,
            )
        ]

    def changeFill(self, fill):
        self.fill = fill
        self.children[0].fillColor = self.fill
        self.draw()

    def getSize(self):
        return self.children[0].size

    def setSize(self, size):
        ydiff = size[1] - self.getSize()[1]
        self.size = [size[0] - ydiff / 2 + self.padding, self.size[1]]
        self.padding += ydiff / 2
        self.register()
        self.draw()


class PlayButton(Component):
    def __init__(
        self, window: Window, id: str, radius: int, pos: List[int], onClick=noOp,
    ) -> None:
        super().__init__(window, id, pos, onClick=onClick)
        self.radius = radius
        self.state = "play"

    def register(self):
        self.children = [
            circle.Circle(
                self.window,
                radius=self.radius,
                units="pix",
                colorSpace="rgb255",
                fillColor=GREEN,
                pos=self.pos,
            ),
            circle.Polygon(
                self.window,
                radius=self.radius / 1.7,
                fillColor=WHITE,
                units="pix",
                pos=self.pos,
                ori=90,
            ),
        ]

    def toggle(self):
        self.state = "stop" if self.state == "play" else "play"
        self.children[1].edges = 3 if self.state == "play" else 4
        self.children[1].ori = 90 if self.state == "play" else 45
        self.children[0].fillColor = GREEN if self.state == "play" else RED
