import math
from typing import Any, Dict

from src.components.core import Component, Panel, Switch
from .expandable_input import ExpandableInput
from .core.input import TextInput
from src.constants import PARAMETER_TYPES_MAP, CYCLEABLE_PARAMETERS, COLORS
from src.utils import paramLabelWithUnits


class ParametersPanel(Component):
    def __init__(self, *args, callback: Any, initialParams: Dict, **kwargs,) -> None:
        super().__init__(*args, listenForKeyPresses=True, **kwargs)
        self.callback = callback
        self.params = initialParams

    def helper(self, k, x):
        if k not in self.params:
            return None
        if x == "":
            return self.params[k]
        return x

    def makeFunc(self, k):
        return lambda x: self.callback(k, self.helper(k, x))

    def register(self):
        l = len(self.params.keys())
        self.children = [
            Panel(
                self.window,
                self.id,
                labelText="stimulus parameters",
                pos=self.pos,
                children=[
                    Switch(
                        self.window,
                        f"{'-'.join(k.split(' '))}-switch",
                        text=paramLabelWithUnits(k),
                        value=v,
                        pos=self.pos,
                        callback=self.makeFunc(k),
                    )
                    if PARAMETER_TYPES_MAP[k] == bool
                    else (ExpandableInput if k in CYCLEABLE_PARAMETERS else TextInput)(
                        self.window,
                        f"{'-'.join(k.split(' '))}-input",
                        value=v,
                        labelText=paramLabelWithUnits(k),
                        pos=self.pos,
                        onChange=self.makeFunc(k),
                        zIndex=l - i,
                    )
                    for i, (k, v) in enumerate(self.params.items())
                ],
                rows=math.ceil(l / 2),
                listenForKeyPresses=self.listenForKeyPresses,
                fill=COLORS["lightgrey"],
            )
        ]
        for c in self.children:
            c.register()

    def resetParams(self, params: Dict) -> None:
        self.params = params
        self.register()
