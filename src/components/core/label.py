from typing import List
from src.window import Window
from src.components.core import Component
from .textbox import Textbox
from src.constants import LIGHTGREY, DARKGREY


class Label(Component):
    def __init__(self, *args, text: str, **kwargs,) -> None:
        super().__init__(*args, **kwargs)
        self.text = text

    def register(self):
        self.children = [
            Textbox(
                self.window,
                self.id,
                pos=self.pos,
                text=f"  {self.text} ",
                fontSize=14,
                color=DARKGREY,
                fill=LIGHTGREY,
                bold=True,
                padding=2,
            )
        ]
        x = self.pos[0] - (self.size[0] / 2) + (self.children[0].size[0] / 2)
        y = self.pos[1] + (self.size[1] / 2) + (self.children[0].size[1] / 2)
        self.children[0].setPos([x, y])
