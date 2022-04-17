from typing import Any, Dict, List

from psychopy.visual import Window

from components import Panel, Button
from .input import TextInput
from constants import WHITE, RED, GREEN


class SyncPanel:
    def __init__(
        self, window: Window, pos: List[int], callback: Any, initialParams: Dict
    ) -> None:
        self.window = window
        self.pos = pos
        self.callback = callback
        self.initialParams = initialParams
        self.syncStatus = initialParams["sync status"]

    def onStatusClicked(self, args: Any):
        self.syncStatus = 1 - self.syncStatus
        self.callback("sync status", self.syncStatus)
        self.register()

    def register(self):
        def makeFunc(k):
            return lambda x: self.callback(k, float(x))

        self.panel = Panel(
            self.window,
            "sync-parameters",
            "sync parameters",
            self.pos,
            children=[
                Button(
                    self.window,
                    "sync-button",
                    f"sync status: {('OFF','ON')[self.syncStatus]}",
                    (RED, GREEN)[self.syncStatus],
                    WHITE,
                    self.pos,
                    bold=True,
                    onClick=self.onStatusClicked,
                )
            ]
            + [
                TextInput(
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

        self.panel.register()

    def draw(self):
        self.panel.draw()

    def contains(self, x):
        return self.panel.contains(x)

    def onClick(self, mouse):
        self.panel.onClick(mouse)

    def onKeyPress(self, key):
        self.panel.onKeyPress(key)
