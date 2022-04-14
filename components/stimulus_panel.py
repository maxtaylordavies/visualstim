from typing import Any, List

from psychopy.visual import Window

from constants import MEDIUMGREY, GREEN, WHITE
from components import Panel, Button


class StimulusPanel:
    def __init__(self, window: Window, pos: List[int], callback: Any) -> None:
        self.window = window

        def onClick(button: Button):
            for i, c in enumerate(self.panel.children):
                if isinstance(c, Button) and list(c.shape.fillColor) == GREEN:
                    self.panel.children[i].shape.fillColor = MEDIUMGREY
                self.panel.children[i].draw()
            button.shape.fillColor = GREEN
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

    def register(self):
        self.panel.register()

    def draw(self):
        self.panel.draw()

    def contains(self, x):
        return self.panel.contains(x)

    def onClick(self, mouse):
        self.panel.onClick(mouse)
