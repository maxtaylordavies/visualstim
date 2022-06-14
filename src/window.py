from typing import List

from psychopy.visual import Window as _Window

from src.constants import WHITE


class Window(_Window):
    def __init__(self, size=[1000, 650], screenNum=0, fullscreen=False) -> None:
        super().__init__(
            size=size,
            screen=screenNum,
            fullscr=fullscreen,
            units="pix",
            color=WHITE,
            colorSpace="rgb255",
        )
        self.components = []

    def assignComponents(self, components: List, activate=False) -> None:
        self.components = components
        if activate:
            self.activateComponents()

    def activateComponents(self) -> None:
        self._toDraw = self.components

    def clearComponents(self) -> None:
        self._toDraw = []
