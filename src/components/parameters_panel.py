from typing import Any, Dict, List

from psychopy.visual import Window

from src.components.core import Component, Panel
from .core.input import Input

# from .text_input import TextInput


class ParametersPanel(Component):
    def __init__(
        self, window: Window, id: str, pos: List[int], callback: Any, initialParams: Dict
    ) -> None:
        self.window = window
        self.id = id
        self.callback = callback

        def makeFunc(k):
            return lambda x: self.callback(k, float(x) if x else initialParams[k])

        self.children = [
            Panel(
                self.window,
                self.id,
                "stimulus parameters",
                pos,
                children=[
                    Input(
                        self.window,
                        f"{'-'.join(k.split(' '))}-input",
                        str(v),
                        k,
                        pos,
                        onChange=makeFunc(k),
                    )
                    for k, v in initialParams.items()
                ],
                rows=2,
            )
        ]
