from typing import Any, Dict

from src.components.core import Component, Panel, Switch
from .core.input import TextInput
from src.utils import paramLabelWithUnits
from src.constants import COLORS


class SyncPanel(Component):
    def __init__(self, *args, callback: Any, initialParams: Dict, **kwargs,) -> None:
        super().__init__(*args, listenForKeyPresses=True, **kwargs)
        self.callback = callback
        self.params = initialParams

    def helper(self, k, x):
        if k not in self.params:
            return None
        if x == "" or x is None:
            return self.params[k]
        return x

    def makeFunc(self, k):
        return lambda x: self.callback(k, self.helper(k, x))

    def register(self):
        self.children = [
            Panel(
                self.window,
                self.id,
                labelText="sync parameters",
                pos=self.pos,
                children=[
                    Switch(
                        self.window,
                        f"{'-'.join(k.split(' '))}-switch",
                        text=paramLabelWithUnits(k),
                        value=v,
                        pos=self.pos,
                        callback=self.makeFunc(k),
                        leftSpaces=11 if k == "sync" else 8,
                    )
                    if type(v) == bool
                    else TextInput(
                        self.window,
                        f"{'-'.join(k.split(' '))}-input",
                        value=v,
                        labelText=paramLabelWithUnits(k),
                        pos=self.pos,
                        onChange=self.makeFunc(k),
                    )
                    for k, v in list(self.params.items())
                ],
                rows=5,
                listenForKeyPresses=self.listenForKeyPresses,
                fill=COLORS["lightgrey"],
            )
        ]

        self.children[0].register()
