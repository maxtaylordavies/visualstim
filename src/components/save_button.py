from typing import Any, List

from psychopy.visual import Window
from psychopy.event import Mouse

from src.components.core import Button, Component
from src.constants import GREEN, PALEGREEN, MEDIUMGREEN, WHITE


class SaveButton(Button):
    def __init__(self, *args, callback: Any, **kwargs) -> None:
        self.saved = False
        self.callback = callback
        super().__init__(
            *args,
            "save-button",
            text=" save ",
            color=GREEN,
            fill=PALEGREEN,
            onClick=self.onClick,
            **kwargs
        )

    def setUnsaved(self):
        if self.saved:
            self.toggle()

    def toggle(self):
        self.saved = not self.saved
        self.text = "saved" if self.saved else " save "
        self.color = MEDIUMGREEN if self.saved else GREEN
        self.fill = WHITE if self.saved else PALEGREEN
        self.register()
        self.draw()

    def onClick(self, *args):
        if self.saved:
            return
        self.callback()
        self.toggle()

