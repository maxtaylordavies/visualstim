from typing import Any, Dict, List

from psychopy.visual import Window
from psychopy.event import Mouse

from src.components.core import Component, Panel, Button
from .core.input import Input
from src.constants import PALEGREEN, PALERED, RED, GREEN


class SyncPanel(Component):
    def __init__(
        self, window: Window, pos: List[int], callback: Any, initialParams: Dict
    ) -> None:
        self.window = window
        self.pos = pos
        self.callback = callback
        self.initialParams = initialParams
        self.syncStatus = initialParams["sync status"]

    def onStatusClicked(self, mouse: Mouse, button: Button):
        self.syncStatus = 1 - self.syncStatus
        self.callback("sync status", self.syncStatus)
        self.register()

    def register(self):
        def makeFunc(k):
            print(self.initialParams[k])
            return lambda x: self.callback(k, float(x) if x else self.initialParams[k])

        self.children = [
            Panel(
                self.window,
                "sync-parameters",
                "sync parameters",
                self.pos,
                children=[
                    Button(
                        self.window,
                        "sync-button",
                        f"  sync status: {('OFF','ON')[self.syncStatus]}",
                        (RED, GREEN)[self.syncStatus],
                        (PALERED, PALEGREEN)[self.syncStatus],
                        self.pos,
                        bold=True,
                        onClick=self.onStatusClicked,
                    )
                ]
                + [
                    Input(
                        self.window,
                        f"{'-'.join(k.split(' '))}-input",
                        str(v),
                        k,
                        self.pos,
                        onChange=makeFunc(k),
                    )
                    for k, v in list(self.initialParams.items())[1:]
                ],
                rows=2,
            )
        ]

        self.children[0].register()
