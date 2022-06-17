from typing import List

from psychopy.visual import Window as _Window

from src.constants import COLORS


class Window(_Window):
    def __init__(self, size=[1000, 650], screenNum=0, fullscreen=False) -> None:
        super().__init__(
            size=size,
            screen=screenNum,
            fullscr=fullscreen,
            units="pix",
            color=COLORS["white"],
            colorSpace="rgb255",
        )
        self.components = []
        self.frameRate = self.getActualFrameRate()

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
