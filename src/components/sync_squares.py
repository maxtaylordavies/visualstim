import platform

from src.constants import COLORS
from src.components.core import Component, Box


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
                color=COLORS["black"],
            ),
            Box(
                self.window,
                f"{self.id}-1",
                pos=[
                    (-self.window.size[0] / factor) + size / 2,
                    (-self.window.size[1] / factor) + size / 2,
                ],
                size=[size, size],
                color=COLORS["black"],
            ),
        ]

    def toggle(self, i):
        if i >= len(self.children):
            return
        self.children[i].changeColor(
            COLORS["white"]
            if self.children[i].color == COLORS["black"]
            else COLORS["black"]
        )

    def turn_off(self, i):
        if i >= len(self.children):
            return
        self.children[i].changeColor(COLORS["black"])
