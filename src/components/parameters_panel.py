import math
from typing import Any, Dict, List

from psychopy.visual import Window

from src.components.core import Component, Panel, Switch
from .core.input import TextInput


class ParametersPanel(Component):
    def __init__(
        self,
        window: Window,
        id: str,
        pos: List[int],
        callback: Any,
        initialParams: Dict,
    ) -> None:
        self.window = window
        self.id = id
        self.pos = pos
        self.callback = callback
        self.params = initialParams

    def cast(self, k, x):
        if k not in self.params:
            return None
        if x == "":
            return self.params[k]
        return type(self.params[k])(x)

    def makeFunc(self, k):
        return lambda x: self.callback(k, self.cast(k, x))

    def register(self):
        self.children = [
            Panel(
                self.window,
                self.id,
                "stimulus parameters",
                self.pos,
                children=[
                    Switch(
                        self.window,
                        f"{'-'.join(k.split(' '))}-switch",
                        k,
                        v,
                        self.pos,
                        self.makeFunc(k),
                    )
                    if type(v) == bool
                    else TextInput(
                        self.window,
                        f"{'-'.join(k.split(' '))}-input",
                        str(v),
                        k,
                        self.pos,
                        onChange=self.makeFunc(k),
                    )
                    for k, v in list(self.params.items())
                ],
                rows=math.ceil(len(self.params.keys()) / 2),
            )
        ]
        for c in self.children:
            c.register()

    def resetParams(self, params: Dict) -> None:
        self.params = params
        self.register()
