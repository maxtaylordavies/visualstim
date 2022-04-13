from typing import Any, List

from constants import LIGHTGREY
from .buttons import Button
from .box import Box
from .label import Label


class Panel:
    def __init__(
        self, id: str, label: str, pos: List[int], size: List[int], children: List[Any],
    ) -> None:
        self.id = id
        self.label = label
        self.pos = pos
        self.size = size

        self.box = Box(f"{id}-box", LIGHTGREY, self.pos, self.size)
        self.label = Label(f"{id}-label", self.label, self.pos, self.size)
        self.children = children

    def register(self, window):
        self.box.register(window)
        self.label.register(window)
        for c in self.children:
            c.register(window)

    def draw(self):
        self.box.draw()
        self.label.draw()
        for c in self.children:
            c.draw()

    def contains(self, x):
        return self.box.contains(x)

    def onClick(self, mouse):
        for c in self.children:
            if c.contains(mouse) and hasattr(c, "onClick"):
                c.onClick(c)
                return
            elif hasattr(c, "active") and c.active:
                c.toggle()

    def onKeyPress(self, key):
        for c in self.children:
            if hasattr(c, "onKeyPress"):
                c.onKeyPress(key)
