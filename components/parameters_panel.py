from typing import Any, Dict, List

from psychopy.visual import Window

from components import Panel
from .input import TextInput


class ParametersPanel:
    def __init__(
        self, window: Window, pos: List[int], callback: Any, initialParams: Dict
    ) -> None:
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
                    f"{'-'.join(k.split(' '))}-input",
                    str(v),
                    k,
                    pos,
                    lambda x: self.callback(k, float(x)),
                )
                for k, v in initialParams.items()
            ],
            rows=2,
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
