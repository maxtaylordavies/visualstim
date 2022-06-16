import platform
from typing import List

from src.window import Window
from src.constants import BLACK, WHITE
from src.components.core import Component, Box
from src.utils import log


class SyncSquares(Component):
    def __init__(self, *args, size=30, **kwargs) -> None:
        super().__init__(*args, **kwargs)

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
                pos=[
                    (-self.window.size[0] / factor) + size / 2,
                    (-self.window.size[1] / factor) + (size * (3 / 2)),
                ],
                size=[size, size],
                color=BLACK,
            ),
            Box(
                self.window,
                f"{self.id}-1",
                pos=[
                    (-self.window.size[0] / factor) + size / 2,
                    (-self.window.size[1] / factor) + size / 2,
                ],
                size=[size, size],
                color=BLACK,
            ),
        ]

    def toggle(self, i):
        log("toggling")
        if i >= len(self.children):
            return
        self.children[i].changeColor(
            WHITE if self.children[i].color == BLACK else BLACK
        )

    def turn_off(self, i):
        if i >= len(self.children):
            return
        self.children[i].changeColor(BLACK)
