from typing import List
from psychopy.visual import Window, TextBox2

from src.components.core import Component
from src.constants import LIGHTGREY, DARKGREY


class Label(Component):
    def __init__(
        self, window: Window, id: str, text: str, pos: List[int], size: List[int],
    ) -> None:
        super().__init__(window, id, pos, size)
        self.text = text

    def register(self):
        self.children = [
            TextBox2(
                self.window,
                f"  {self.text} ",
                "Open Sans",
                units="pix",
                letterHeight=14,
                colorSpace="rgb255",
                color=DARKGREY,
                fillColor=LIGHTGREY,
                bold=True,
                padding=2,
                size=[None, None],
            )
        ]
        x = self.pos[0] - (self.size[0] / 2) + (self.children[0].size[0] / 2)
        y = self.pos[1] + (self.size[1] / 2) + (self.children[0].size[1] / 2)
        self.children[0].pos = [x, y]
