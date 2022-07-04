import math

from src.components.core import Component, Box, Label


class Panel(Component):
    def __init__(self, *args, labelText: str, rows=1, padding=15, **kwargs,) -> None:
        super().__init__(*args, **kwargs)
        self.labelText = labelText
        self.rows = rows
        self.padding = padding

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
                r * childrenPerRow, min((r + 1) * childrenPerRow, len(self.children))
            ):
                x += self.children[i].getSize()[0] / 2 + padding
                self.children[i].pos = [x, y]
                x += self.children[i].getSize()[0] / 2
            y -= self.children[0].getSize()[1] / 2

        self.box = Box(
            self.window,
            f"{self.id}-box",
            pos=self.pos,
            size=self.size,
            color=self.fill,
        )
        children = [self.box]

        if labelText:
            children.append(
                Label(
                    self.window,
                    f"{self.id}-label",
                    text=self.labelText,
                    pos=self.pos,
                    size=self.size,
                )
            )

        self.children = children + self.children
