from typing import Any, List

from psychopy.visual import Window
from psychopy.event import Mouse

from constants import MEDIUMGREY, GREEN, WHITE
from components import Component, Panel, Button


class StimulusPanel(Component):
    def __init__(self, window: Window, pos: List[int], callback: Any) -> None:
        self.window = window

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
            "select-stimulus",
            "stimulus type",
            pos,
            children=[
                Button(
                    self.window,
                    "stimtype-drifting-grating",
                    "drifting grating",
                    WHITE,
                    GREEN,
                    pos,
                    padding=5,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-static-grating",
                    "static grating",
                    WHITE,
                    MEDIUMGREY,
                    pos,
                    padding=5,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-movie",
                    "    movie   ",
                    WHITE,
                    MEDIUMGREY,
                    pos,
                    padding=5,
                    onClick=onClick,
                ),
            ],
        )
        self.children = [self.panel]
