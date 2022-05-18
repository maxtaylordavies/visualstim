import platform
from typing import List

from psychopy.visual import Window

from src.constants import BLACK, WHITE
from src.components.core import Component, Box


class SyncSquares(Component):
    def __init__(self, window: Window, id: str, size=30) -> None:
        super().__init__(window, id)

        # not sure why, but (in my experience) on Mac the left edge
        # of the PsychoPy window is at -window_width/4; on Windows
        # it's at -window_width/2. Similar for bottom edge
        # so in order to correctly position the sync/trigger squares in
        # the bottom left corner, we need to check what platform we're on
        factor = 2 if platform.system() == "Windows" else 4

        self.children = [
            Box(
                self.window,
                f"{self.id}-0",
                BLACK,
                [
                    (-self.window.size[0] / factor) + size / 2,
                    (-self.window.size[1] / factor) + (size * (3 / 2)),
                ],
                [size, size],
            ),
            Box(
                self.window,
                f"{self.id}-1",
                BLACK,
                [
                    (-self.window.size[0] / factor) + size / 2,
                    (-self.window.size[1] / factor) + size / 2,
                ],
                [size, size],
            ),
        ]

    def toggle(self, i):
        if i >= len(self.children):
            return
        self.children[i].changeColor(
            WHITE if self.children[i].color == BLACK else BLACK
        )

    def turn_off(self, i):
        if i >= len(self.children):
            return
        self.children[i].changeColor(BLACK)
