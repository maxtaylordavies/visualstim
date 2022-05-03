from typing import List

from psychopy.visual import Window

from src.constants import BLACK, WHITE
from src.components.core import Component, Box


class SyncSquares(Component):
    def __init__(self, window: Window, id: str, size=30) -> None:
        self.window = window
        self.id = id
        self.children = [
            Box(
                self.window,
                f"{self.id}-0",
                BLACK,
                [
                    (-self.window.size[0] / 2) + size / 2,
                    (-self.window.size[1] / 2) + (size * (3 / 2)),
                ],
                [size, size],
            ),
            Box(
                self.window,
                f"{self.id}-1",
                BLACK,
                [
                    (-self.window.size[0] / 2) + size / 2,
                    (-self.window.size[1] / 2) + size / 2,
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
