from typing import Iterable, List

from psychopy.visual import Window as _Window

from src.constants import COLORS
from src.components.core import Box, Component, Textbox

SYNC_SQUARE_SIZE = 30


class Window(_Window):
    def __init__(
        self, screenNum=0, fullscreen=False, color=COLORS["white"], sync=False, **kwargs
    ) -> None:
        super().__init__(
            screen=screenNum,
            fullscr=fullscreen,
            units="pix",
            color=color,
            colorSpace="rgb255",
            **kwargs,
        )

        print(f"self.color: {self.color}")

        self.fullscreen = fullscreen
        self.sync = sync
        self.components = []
        self.frameRate = self.getActualFrameRate() or 30

        self.scaleFactor = (
            self.size[0] / self.clientSize[0]
        ) * self.getContentScaleFactor()
        self.compressionFactor = 2

        # create sync squares
        self.createSyncSquares()

    def createSyncSquares(self):
        self.syncSquares = Component(
            self,
            "sync-squares",
            children=[
                Box(
                    self,
                    "sync-squares-0",
                    pos=[
                        (-self.size[0] / self.scaleFactor) + SYNC_SQUARE_SIZE / 2,
                        (-self.size[1] / self.scaleFactor)
                        + (SYNC_SQUARE_SIZE * (3 / 2)),
                    ],
                    size=[SYNC_SQUARE_SIZE, SYNC_SQUARE_SIZE],
                    color=COLORS["black"],
                ),
                Box(
                    self,
                    "sync-squares-1",
                    pos=[
                        (-self.size[0] / self.scaleFactor) + SYNC_SQUARE_SIZE / 2,
                        (-self.size[1] / self.scaleFactor) + SYNC_SQUARE_SIZE / 2,
                    ],
                    size=[SYNC_SQUARE_SIZE, SYNC_SQUARE_SIZE],
                    color=COLORS["black"],
                ),
            ],
            hide=not self.sync,
        )
        self.syncSquares.register()

    def reportProgress(self, iterable: Iterable, description: str, interval=10):
        return ReportProgress(iterable, self, description, interval=interval)

    def assignComponents(self, components: List, activate=False) -> None:
        self.components = components
        if activate:
            self.activateComponents()

    def activateComponents(self) -> None:
        self._toDraw = self.components

    def clearComponents(self) -> None:
        self._toDraw = []

    def setBackgroundColor(self, color: List[int]) -> None:
        print(f"setting background color: {color}")
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


class ReportProgress(object):
    def __init__(
        self, iterable: Iterable, window: Window, description: str, interval=10
    ) -> None:
        self.iterable = iterable
        self.window = window
        self.description = description
        self.len = len(self.iterable)
        self.index = 0
        self.interval = interval

        self.textbox = Textbox(
            self.window,
            "progress-message",
            text=f"{self.description}: 100%",
            color=COLORS["black"],
            fontSize=16,
            zIndex=100,
            padding=10,
        )
        self.textbox.register()
        self.computePos()
        self.renderProgress()

    def __iter__(self):
        for obj in self.iterable:
            yield obj
            if self.index % self.interval == 0:
                self.renderProgress()
            self.index += 1

    def renderProgress(self):
        msg = (
            "done!"
            if self.index == self.len
            else f"{int(100 * (self.index / self.len))}%"
        )
        self.textbox.setText(f"{self.description}: {msg}")

        self.textbox.draw()
        self.window.flip()

    def computePos(self):
        width, height = self.textbox.size
        self.textbox.setPos(
            [
                (self.window.size[0] / self.window.scaleFactor) - (width / 2) + 20,
                (-self.window.size[1] / self.window.scaleFactor) + height / 2,
            ]
        )
