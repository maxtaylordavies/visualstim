import math
from typing import Any, Dict, List

from psychopy.visual import Window

from .expandable_input import ExpandableInput
from src.components.core import Component, Panel, Switch
from .core.input import TextInput
from src.constants import CYCLEABLE_PARAMETERS


class ParametersPanel(Component):
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
                    else (ExpandableInput if k in CYCLEABLE_PARAMETERS else TextInput)(
                        self.window,
                        f"{'-'.join(k.split(' '))}-input",
                        v,
                        k,
                        self.pos,
                        onChange=self.makeFunc(k),
                        zIndex=l - i,
                    )
                    for i, (k, v) in enumerate(self.params.items())
                ],
                rows=math.ceil(l / 2),
            )
        ]
        for c in self.children:
            c.register()

    def resetParams(self, params: Dict) -> None:
        self.params = params
        self.register()
