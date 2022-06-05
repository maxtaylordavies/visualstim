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
        labelText: str,
        pos: List[int],
        children: List[Any],
        rows=1,
        padding=15,
        background=LIGHTGREY,
        **kwargs,
    ) -> None:
        super().__init__(window, id, pos=pos, children=children, **kwargs)
        self.labelText = labelText
        self.rows = rows
        self.padding = padding
        self.background = background

        super().register()

        childrenPerRow = math.ceil(len(self.children) / self.rows)

        if self.rows > 1:
            maxChildWidth = max(map(lambda c: c.getSize()[0], self.children))
            maxChildHeight = max(map(lambda c: c.getSize()[1], self.children))
            for i in range(len(self.children)):
                self.children[i].setSize([maxChildWidth, maxChildHeight])

            width = (childrenPerRow * (maxChildWidth + 15)) + 15

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

        # position children automatically in grid layout
        y = self.pos[1] + (self.size[1] / 2)
        for r in range(self.rows):
            x = self.pos[0] - (self.size[0] / 2)
            y -= (self.children[0].getSize()[1] / 2) + padding
            for i in range(
                r * childrenPerRow, min((r + 1) * childrenPerRow, len(children))
            ):
                x += self.children[i].getSize()[0] / 2 + padding
                self.children[i].pos = [x, y]
                x += self.children[i].getSize()[0] / 2
            y -= self.children[0].getSize()[1] / 2

        self.box = Box(self.window, f"{id}-box", self.background, self.pos, self.size)
        children = [self.box]

        if labelText:
            children.append(
                Label(self.window, f"{id}-label", self.labelText, self.pos, self.size)
            )

        self.children = children + self.children
