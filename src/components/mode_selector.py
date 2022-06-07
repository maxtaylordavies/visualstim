from typing import Any, List

from psychopy.visual import Window

from src.components.core import Component, Box, Textbox
from src.constants import LIGHTGREY, DARKGREY, GREY


class ModeSelector(Component):
    def __init__(self, *args, mode: str, callback: Any, **kwargs,) -> None:
        super().__init__(*args, **kwargs)
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
                pos=[self.pos[0] - 50, self.pos[1]],
                text="interactive",
                color=(GREY, DARKGREY)[self.mode == "interactive"],
                fill=LIGHTGREY,
                bold=self.mode == "interactive",
                padding=2,
                fontSize=16,
            ),
            Textbox(
                self.window,
                f"{self.id}-scripting",
                pos=[self.pos[0] + 28, self.pos[1]],
                text="scripting",
                color=(GREY, DARKGREY)[self.mode == "scripting"],
                fill=LIGHTGREY,
                bold=self.mode == "scripting",
                padding=2,
                fontSize=16,
            ),
            Box(
                self.window,
                f"{self.id}-underline",
                pos=[
                    self.pos[0] + (-52 if self.mode == "interactive" else 26),
                    self.pos[1] - 11,
                ],
                size=[80 if self.mode == "interactive" else 65, 2],
                color=DARKGREY,
            ),
        ]
        super().register()
