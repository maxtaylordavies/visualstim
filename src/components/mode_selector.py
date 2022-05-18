from typing import Any, List

from psychopy.visual import Window, TextBox2
from psychopy.event import Mouse

from src.components.core import Component, Box
from src.constants import DARKGREY, GREY


class ModeSelector(Component):
    def __init__(
        self, window: Window, id: str, pos: List[int], mode: str, callback: Any
    ) -> None:
        super().__init__(window, id, pos)
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
                color=(GREY, DARKGREY)[self.mode == "interactive"],
                bold=self.mode == "interactive",
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
                color=(GREY, DARKGREY)[self.mode == "scripting"],
                bold=self.mode == "scripting",
                padding=2,
                pos=[self.pos[0] + 28, self.pos[1]],
                size=[None, None],
            ),
            Box(
                self.window,
                f"{self.id}-underline",
                DARKGREY,
                [
                    self.pos[0] + (-52 if self.mode == "interactive" else 26),
                    self.pos[1] - 11,
                ],
                [80 if self.mode == "interactive" else 65, 2],
            ),
        ]
        self.children[-1].register()

    def onClick(self, mouse: Mouse, component: Any) -> None:
        self.callback()
