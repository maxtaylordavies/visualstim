from typing import List

from psychopy.visual import Window as _Window

from src.constants import COLORS, PIXEL_FACTOR
from src.components.core import Box, Component

SYNC_SQUARE_SIZE = 30


class Window(_Window):
    def __init__(
        self, size=[1000, 650], screenNum=0, fullscreen=False, sync=False
    ) -> None:
        super().__init__(
            size=size,
            screen=screenNum,
            fullscr=fullscreen,
            units="pix",
            color=COLORS["white"],
            colorSpace="rgb255",
        )
        self.fullscreen = fullscreen
        self.components = []
        self.frameRate = self.getActualFrameRate() or 30

        ## create sync squares
        self.syncSquares = Component(
            self,
            "sync-squares",
            children=[
                Box(
                    self,
                    "sync-squares-0",
                    pos=[
                        (-self.size[0] / PIXEL_FACTOR) + SYNC_SQUARE_SIZE / 2,
                        (-self.size[1] / PIXEL_FACTOR) + (SYNC_SQUARE_SIZE * (3 / 2)),
                    ],
                    size=[SYNC_SQUARE_SIZE, SYNC_SQUARE_SIZE],
                    color=COLORS["black"],
                ),
                Box(
                    self,
                    "sync-squares-1",
                    pos=[
                        (-self.size[0] / PIXEL_FACTOR) + SYNC_SQUARE_SIZE / 2,
                        (-self.size[1] / PIXEL_FACTOR) + SYNC_SQUARE_SIZE / 2,
                    ],
                    size=[SYNC_SQUARE_SIZE, SYNC_SQUARE_SIZE],
                    color=COLORS["black"],
                ),
            ],
            hide=not sync,
        )
        self.syncSquares.register()

    def assignComponents(self, components: List, activate=False) -> None:
        self.components = components
        if activate:
            self.activateComponents()

    def activateComponents(self) -> None:
        self._toDraw = self.components

    def clearComponents(self) -> None:
        self._toDraw = []

    def setBackgroundColor(self, color: List[int]) -> None:
        self.color = color

    def setShowSyncSquares(self, show: bool) -> None:
        self.syncSquares.setHidden(not show, propagate=True)

    def toggleSyncSquare(self, i: int) -> None:
        if i >= len(self.syncSquares.children):
            return
        self.syncSquares.children[i].changeColor(
            COLORS["white"]
            if self.syncSquares.children[i].color == COLORS["black"]
            else COLORS["black"]
        )

    def turnOffSyncSquare(self, i: int) -> None:
        if i >= len(self.syncSquares.children):
            return
        self.syncSquares.children[i].changeColor(COLORS["black"])

    def flip(self):
        if hasattr(self, "syncSquares"):
            self.syncSquares.draw()
        super().flip()
