from typing import List

from psychopy.visual import Window

from constants import BLACK, WHITE
from components import Box


class SyncSquares:
    def __init__(self, window: Window, id: str, size=30) -> None:
        self.window = window
        self.id = id
        self.squares = [
            Box(
                self.window,
                f"{self.id}-0",
                BLACK,
                [
                    (-self.window.size[0] / 4) + size / 2,
                    (-self.window.size[1] / 4) + (size * (3 / 2)),
                ],
                [size, size],
            ),
            Box(
                self.window,
                f"{self.id}-1",
                BLACK,
                [
                    (-self.window.size[0] / 4) + size / 2,
                    (-self.window.size[1] / 4) + size / 2,
                ],
                [size, size],
            ),
        ]

    def register(self):
        for sq in self.squares:
            sq.register()

    def draw(self):
        for sq in self.squares:
            sq.draw()

    def contains(self, x):
        for sq in self.squares:
            if sq.contains(x):
                return True
        return False

    def toggle(self, i):
        if i >= len(self.squares):
            return
        self.squares[i].changeColor(WHITE if self.squares[i].color == BLACK else BLACK)

    def onClick(self, args):
        self.toggle(0)
