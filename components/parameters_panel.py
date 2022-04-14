from typing import Any, List

from psychopy.visual import Window

from constants import MEDIUMGREY, GREEN, WHITE
from components import Panel
from .input import TextInput


class ParametersPanel:
    def __init__(self, window: Window, pos: List[int], callback: Any) -> None:
        self.window = window
        self.callback = callback
        self.panel = Panel(
            self.window,
            "select-parameters",
            "parameters",
            pos,
            children=[
                TextInput(
                    self.window,
                    "spatial-frequency-input",
                    "10",
                    "spatial freq",
                    pos,
                    lambda x: self.callback("spatial frequency", float(x)),
                ),
                TextInput(
                    self.window,
                    "temporal-frequency-input",
                    "10",
                    "temporal freq",
                    pos,
                    lambda x: self.callback("temporal frequency", float(x)),
                ),
            ],
        )

    def register(self):
        self.panel.register()

    def draw(self):
        self.panel.draw()

    def contains(self, x):
        return self.panel.contains(x)

    def onClick(self, mouse):
        self.panel.onClick(mouse)

    def onKeyPress(self, key):
        self.panel.onKeyPress(key)
