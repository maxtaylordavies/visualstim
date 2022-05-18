from typing import Any, List

from src.constants import RED, GREEN, PALERED, PALEGREEN
from src.components.core import Component, Button

from psychopy.visual import Window
from psychopy.event import Mouse


class Switch(Component):
    def __init__(
        self,
        window: Window,
        id: str,
        text: str,
        value: bool,
        pos: List[int],
        callback: Any,
    ):
        super().__init__(window, id, pos)
        self.text = text
        self.value = value
        self.callback = callback
        self.padding = 2

    def onClick(self, mouse: Mouse, button: Button):
        self.value = not self.value
        self.callback(self.value)
        self.register()

    def register(self):
        self.children = [
            Button(
                self.window,
                self.id,
                f"      {self.text}: {('FALSE','TRUE')[int(self.value)]}",
                (RED, GREEN)[int(self.value)],
                (PALERED, PALEGREEN)[int(self.value)],
                self.pos,
                bold=True,
                onClick=self.onClick,
                size=self.size,
                padding=self.padding,
            )
        ]
        super().register()

    def getSize(self):
        return self.children[0].getSize()

    def setSize(self, size):
        ydiff = size[1] - self.getSize()[1]
        self.size = [size[0] - ydiff / 2 + self.padding, self.size[1]]
        self.padding += ydiff / 2
        self.register()
        self.draw()

