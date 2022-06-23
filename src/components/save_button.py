from typing import Any

from src.components.core import Button
from src.constants import COLORS


class SaveButton(Button):
    def __init__(self, *args, callback: Any, **kwargs) -> None:
        self.saved = False
        self.callback = callback
        super().__init__(
            *args,
            "save-button",
            text=" save ",
            color=COLORS["green"],
            fill=COLORS["palegreen"],
            onClick=self.onClick,
            **kwargs
        )

    def setUnsaved(self):
        if self.saved:
            self.toggle()

    def toggle(self):
        self.saved = not self.saved
        self.text = "saved" if self.saved else " save "
        self.color = COLORS["mediumgreen"] if self.saved else COLORS["green"]
        self.fill = COLORS["white"] if self.saved else COLORS["palegreen"]
        self.register()
        self.draw()

    def onClick(self, *args):
        if self.saved:
            return
        self.callback()
        self.toggle()

