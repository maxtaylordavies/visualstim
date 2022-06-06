from typing import List

from psychopy.visual import TextBox2

from src.components.core import Component
from src.constants import WHITE
from src.utils import log


class Box(Component):
    def __init__(
        self, *args, borderColor: List[int] = WHITE, borderWidth: int = 0, **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.borderColor = borderColor
        self.borderWidth = borderWidth

    def register(self):
        self.children = [
            TextBox2(
                self.window,
                units="pix",
                colorSpace="rgb255",
                fillColor=self.color,
                size=self.size,
                pos=self.pos,
                text="",
                font="Open Sans",
                borderColor=self.borderColor,
                borderWidth=self.borderWidth,
            )
        ] + self.children
        super().register()

    def changeColor(self, color: List[int], draw=True):
        self.color = color
        self.children[0].fillColor = self.color
        if draw:
            self.draw()
