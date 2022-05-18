from typing import Any, Dict, List

from psychopy.visual import Window
from psychopy.event import Mouse

from src.components.core import Component, Panel, Button, Switch
from .core.input import TextInput
from src.constants import PALEGREEN, PALERED, RED, GREEN


class SyncPanel(Component):
    def __init__(
        self,
        window: Window,
        id: str,
        pos: List[int],
        callback: Any,
        initialParams: Dict,
    ) -> None:
        super().__init__(window, id, pos)
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
                "sync parameters",
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
                rows=4,
            )
        ]

        self.children[0].register()
