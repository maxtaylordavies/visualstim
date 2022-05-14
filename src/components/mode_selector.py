from typing import Any, List

from psychopy.visual import Window, TextBox2
from psychopy.event import Mouse

from src.components.core import Component
from src.constants import BLACK, GREY


class ModeSelector(Component):
    def __init__(
        self, window: Window, id: str, pos: List[int], mode: str, callback: Any
    ) -> None:
        self.window = window
        self.id = id
        self.pos = pos
        self.mode = mode
        self.callback = callback

    def register(self) -> None:
        self.children = [
            TextBox2(
                self.window,
                "interactive",
                "Open Sans",
                alignment="center",
                units="pix",
                letterHeight=16,
                colorSpace="rgb255",
                color=(GREY, BLACK)[self.mode == "interactive"],
                padding=2,
                pos=[self.pos[0] - 50, self.pos[1]],
                size=[None, None],
            ),
            TextBox2(
                self.window,
                "scripting",
                "Open Sans",
                alignment="center",
                units="pix",
                letterHeight=16,
                colorSpace="rgb255",
                color=(GREY, BLACK)[self.mode == "scripting"],
                padding=2,
                pos=[self.pos[0] + 30, self.pos[1]],
                size=[None, None],
            ),
        ]

    def onClick(self, mouse: Mouse, component: Any) -> None:
        self.callback()
