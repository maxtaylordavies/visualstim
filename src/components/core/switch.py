from typing import Any, List

from src.constants import RED, GREEN, PALERED, PALEGREEN
from src.components.core import Component, Button

from psychopy.visual import Window
from psychopy.event import Mouse


class Switch(Component):
    def __init__(
        self,
        *args,
        text: str,
        value: bool,
        callback: Any,
        leftSpaces=5,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.text = text
        self.value = value
        self.callback = callback
        self.padding = 2
        self.leftSpaces = leftSpaces

    def onClick(self, *args):
        self.value = not self.value
        self.callback(self.value)
        self.register()

    def register(self):
        self.children = [
            Button(
                self.window,
                self.id,
                text=f"{' ' * self.leftSpaces}{self.text}: {('FALSE','TRUE')[int(self.value)]}",
                color=(RED, GREEN)[int(self.value)],
                fill=(PALERED, PALEGREEN)[int(self.value)],
                pos=self.pos,
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

