import math
from typing import Any, List

from psychopy.visual import Window

from src.components.core import Component, Box, Label
from src.constants import LIGHTGREY


class Panel(Component):
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
        super().__init__(window, id, pos=pos, children=children)
        self.label = label
        self.padding = padding
        self.rows = rows

        super().register()

        childrenPerRow = math.ceil(len(self.children) / self.rows)

        if self.rows > 1:
            maxChildWidth = max(map(lambda c: c.getSize()[0], self.children))
            maxChildHeight = max(map(lambda c: c.getSize()[1], self.children))
            for i in range(len(self.children)):
                self.children[i].setSize([maxChildWidth, maxChildHeight])

            width = (childrenPerRow * (maxChildWidth + self.padding)) + self.padding
            height = (
                self.rows * (self.children[0].getSize()[1] + self.padding)
                + self.padding
            )
        else:
            # compute dimensions of panel based on children
            width = sum(map(lambda c: c.getSize()[0], self.children)) + (
                self.padding * (len(self.children) + 1)
            )
            height = max(map(lambda c: c.getSize()[1], self.children)) + (
                self.padding * 2
            )

        self.size = [width, height]

        # position children automatically
        for r in range(self.rows):
            x = self.pos[0] - (self.size[0] / 2)
            y = (
                self.pos[1]
                + (self.size[1] / 2)
                - (r + 1) * (self.children[0].getSize()[1] / 2)
                - (2 * r + 1) * padding
            )
            for i in range(
                r * childrenPerRow, min((r + 1) * childrenPerRow, len(children))
            ):
                x += self.children[i].getSize()[0] / 2 + padding
                self.children[i].pos = [x, y]
                x += self.children[i].getSize()[0] / 2

        self.box = Box(self.window, f"{id}-box", LIGHTGREY, self.pos, self.size)
        self.label = Label(self.window, f"{id}-label", self.label, self.pos, self.size)
        self.children = [self.box, self.label] + self.children
