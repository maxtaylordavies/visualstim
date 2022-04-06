from typing import Any, List
from psychopy.visual import Window, TextBox2


class Button:
    def __init__(
        self, text: str, color: List[int], pos: List[int], onClick: Any
    ) -> None:
        self.text = text
        self.color = color
        self.pos = pos
        self.onClick = onClick

    def register(self, window):
        self.shape = TextBox2(
            window,
            self.text,
            "Open Sans",
            units="pix",
            letterHeight=20,
            colorSpace="rgb255",
            fillColor=self.color,
            color="white",
            bold=True,
            padding=5,
            size=[None, None],
            pos=self.pos,
        )

    def draw(self):
        self.shape.draw()

    def contains(self, x):
        return self.shape.contains(x)
