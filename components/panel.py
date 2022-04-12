from typing import List

from constants import LIGHTGREY
from .buttons import Button
from .box import Box
from .label import Label


class Panel:
    def __init__(
        self,
        id: str,
        label: str,
        pos: List[int],
        size: List[int],
        buttons: List[Button],
    ) -> None:
        self.id = id
        self.label = label
        self.pos = pos
        self.size = size

        self.box = Box(f"{id}-box", LIGHTGREY, self.pos, self.size)
        self.label = Label(f"{id}-label", self.label, self.pos, self.size)
        self.buttons = buttons

    def register(self, window):
        self.box.register(window)
        self.label.register(window)
        for b in self.buttons:
            b.register(window)

    def draw(self):
        self.box.draw()
        self.label.draw()
        for b in self.buttons:
            b.draw()

    def contains(self, x):
        return self.box.contains(x)

    def handleClick(self, mouse):
        for b in self.buttons:
            if b.contains(mouse):
                b.onClick(b)
                return
