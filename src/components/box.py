from typing import List

from psychopy.visual import rect, Window

from src.components import Component


class Box(Component):
    def __init__(
        self,
        window: Window,
        id: str,
        color: List[int],
        pos: List[int],
        size: List[int],
    ) -> None:
        self.window = window
        self.id = id
        self.color = color
        self.pos = pos
        self.size = size

    def register(self):
        self.children = [
            rect.Rect(
                self.window,
                units="pix",
                colorSpace="rgb255",
                fillColor=self.color,
                size=self.size,
                pos=self.pos,
            )
        ]

    def changeColor(self, color: List[int], draw=True):
        self.color = color
        self.register()
        if draw:
            self.draw()
