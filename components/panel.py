import math
from typing import Any, List

from psychopy.visual import Window

from constants import LIGHTGREY
from .buttons import Button
from .box import Box
from .label import Label


class Panel:
    def __init__(
        self,
        window: Window,
        id: str,
        label: str,
        pos: List[int],
        children: List[Any],
        rows=1,
        padding=15,
    ) -> None:
        self.window = window
        self.id = id
        self.label = label
        self.pos = pos
        self.children = children
        self.padding = padding
        self.rows = rows

        for c in self.children:
            c.register()

        childrenPerRow = math.ceil(len(self.children) / self.rows)

        if self.rows > 1:
            maxChildWidth = max(map(lambda c: c.size()[0], self.children))
            maxChildHeight = max(map(lambda c: c.size()[1], self.children))
            for i in range(len(self.children)):
                self.children[i].setSize([maxChildWidth, maxChildHeight])

            width = (childrenPerRow * (maxChildWidth + self.padding)) + self.padding
            height = (
                self.rows * (self.children[0].size()[1] + self.padding) + self.padding
            )
        else:
            # compute dimensions of panel based on children
            width = sum(map(lambda c: c.size()[0], self.children)) + (
                self.padding * (len(self.children) + 1)
            )
            height = max(map(lambda c: c.size()[1], self.children)) + (self.padding * 2)

        self.size = [width, height]

        # position children automatically
        for r in range(self.rows):
            x = self.pos[0] - (self.size[0] / 2)
            y = (
                self.pos[1]
                + (self.size[1] / 2)
                - (r + 1) * (self.children[0].size()[1] / 2)
                - (2 * r + 1) * padding
            )
            for i in range(
                r * childrenPerRow, min((r + 1) * childrenPerRow, len(children))
            ):
                x += self.children[i].size()[0] / 2 + padding
                self.children[i].pos = [x, y]
                x += self.children[i].size()[0] / 2

        self.box = Box(self.window, f"{id}-box", LIGHTGREY, self.pos, self.size)
        self.label = Label(self.window, f"{id}-label", self.label, self.pos, self.size)

    def register(self):
        self.box.register()
        self.label.register()
        for c in self.children:
            c.register()

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
            elif hasattr(c, "active") and c.active:
                c.toggle()

    def onKeyPress(self, key):
        for c in self.children:
            if hasattr(c, "onKeyPress"):
                c.onKeyPress(key)
