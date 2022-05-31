from typing import Any, List

from psychopy.visual import Window
from psychopy.event import Mouse

from src.constants import MEDIUMGREY, GREEN, WHITE
from src.components.core import Component, Panel, Button


class StimulusPanel(Component):
    def __init__(self, window: Window, id: str, pos: List[int], callback: Any) -> None:
        super().__init__(window, id, pos)

        def onClick(mouse: Mouse, button: Button):
            for i, c in enumerate(self.panel.children):
                if isinstance(c, Button) and list(c.fill) == GREEN:
                    self.panel.children[i].changeFill(MEDIUMGREY)
                self.panel.children[i].draw()
            button.changeFill(GREEN)
            button.draw()
            callback(button.text.strip())

        self.panel = Panel(
            self.window,
            self.id,
            "stimulus type",
            self.pos,
            children=[
                Button(
                    self.window,
                    "stimtype-static-grating",
                    "  static grating",
                    WHITE,
                    MEDIUMGREY,
                    self.pos,
                    padding=2,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-drift-grating",
                    "   drift grating",
                    WHITE,
                    GREEN,
                    self.pos,
                    padding=2,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-osc-grating",
                    "    osc grating",
                    WHITE,
                    MEDIUMGREY,
                    self.pos,
                    padding=2,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-movie",
                    "       movie",
                    WHITE,
                    MEDIUMGREY,
                    self.pos,
                    padding=2,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-sparse-noise",
                    "  sparse noise",
                    WHITE,
                    MEDIUMGREY,
                    self.pos,
                    padding=2,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-checkerboard",
                    " checkerboard",
                    WHITE,
                    MEDIUMGREY,
                    self.pos,
                    padding=2,
                    onClick=onClick,
                ),
            ],
            rows=2,
            padding=12.5,
        )
        self.children = [self.panel]
