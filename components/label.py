from typing import List
from psychopy.visual import Window, TextBox2


class Label:
    def __init__(
        self, id: str, text: str, boxPos: List[int], boxSize: List[int],
    ) -> None:
        self.id = id
        self.text = text
        self.boxPos = boxPos
        self.boxSize = boxSize

    def register(self, window: Window):
        self.shape = TextBox2(
            window,
            f"  {self.text} ",
            "Open Sans",
            units="pix",
            letterHeight=14,
            colorSpace="rgb255",
            color=[119, 119, 119],
            fillColor=[230, 230, 230],
            bold=True,
            padding=2,
            size=[None, None],
        )
        x = self.boxPos[0] - (self.boxSize[0] / 2) + (self.shape.size[0] / 2)
        y = self.boxPos[1] + (self.boxSize[1] / 2) + (self.shape.size[1] / 2)
        self.shape.pos = [x, y]

    def draw(self):
        self.shape.draw()
