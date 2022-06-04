from typing import Any, List

from psychopy.visual import Window

from src.components.core import Component, Box, Textbox
from src.constants import DARKGREY, GREY


class ModeSelector(Component):
    def __init__(
        self, window: Window, id: str, pos: List[int], mode: str, callback: Any
    ) -> None:
        super().__init__(window, id, pos)
        self.mode = mode
        self.callback = callback

    def onClick(self, a, b):
        self.mode = ("interactive", "scripting")[self.mode == "interactive"]
        self.register()
        self.callback()

    def register(self) -> None:
        self.children = [
            Textbox(
                self.window,
                f"{self.id}-interactive",
                [self.pos[0] - 50, self.pos[1]],
                "interactive",
                color=(GREY, DARKGREY)[self.mode == "interactive"],
                bold=self.mode == "interactive",
                padding=2,
                fontSize=16,
            ),
            Textbox(
                self.window,
                f"{self.id}-scripting",
                [self.pos[0] + 28, self.pos[1]],
                "scripting",
                color=(GREY, DARKGREY)[self.mode == "scripting"],
                bold=self.mode == "scripting",
                padding=2,
                fontSize=16,
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
        super().register()
