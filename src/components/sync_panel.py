from typing import Any, Dict, List

from psychopy.visual import Window

from src.components.core import Component, Panel, Switch
from .core.input import TextInput
from src.utils import paramLabelWithUnits
from src.constants import LIGHTGREY


class SyncPanel(Component):
    def __init__(self, *args, callback: Any, initialParams: Dict, **kwargs,) -> None:
        super().__init__(*args, listenForKeyPresses=True, **kwargs)
        self.callback = callback
        self.params = initialParams

    def helper(self, k, x):
        if k not in self.params:
            return None
        if not x:
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
                        leftSpaces=11,
                    )
                    if type(v) == bool
                    else TextInput(
                        self.window,
                        f"{'-'.join(k.split(' '))}-input",
                        value=str(v),
                        labelText=paramLabelWithUnits(k),
                        pos=self.pos,
                        onChange=self.makeFunc(k),
                    )
                    for k, v in list(self.params.items())
                ],
                rows=4,
                listenForKeyPresses=self.listenForKeyPresses,
                fill=LIGHTGREY,
            )
        ]

        self.children[0].register()
