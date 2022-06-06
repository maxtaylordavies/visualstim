from typing import List
from psychopy.visual import Window, circle

from src.components.core import Component
from .textbox import Textbox
from src.constants import GREEN, RED, WHITE
from src.utils import noOp


class Button(Component):
    def __init__(self, *args, text="", bold=True, padding=2, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.text = text
        self.bold = bold
        self.padding = padding
        self.borderWidth = 0

    def register(self):
        self.children = [
            Textbox(
                self.window,
                self.id,
                pos=self.pos,
                text=f" {self.text} ",
                color=self.color,
                fill=self.fill,
                bold=self.bold,
                padding=self.padding,
                size=self.size,
            )
        ]

    def changeFill(self, fill):
        self.fill = fill
        self.register()
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
