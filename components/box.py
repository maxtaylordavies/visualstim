from typing import List

from psychopy.visual import rect, Window


class Box:
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
        self.shape = rect.Rect(
            self.window,
            units="pix",
            colorSpace="rgb255",
            fillColor=self.color,
            size=self.size,
            pos=self.pos,
        )

    def draw(self):
        self.shape.draw()

    def contains(self, x):
        return self.shape.contains(x)
