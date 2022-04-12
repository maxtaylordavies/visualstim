from typing import Any, List

from constants import MEDIUMGREY, GREEN, WHITE
from components import Panel, Button


class StimulusPanel:
    def __init__(self, pos: List[int], callback: Any) -> None:
        def onClick(button: Button):
            for i, b in enumerate(self.panel.buttons):
                if list(b.shape.fillColor) == GREEN:
                    self.panel.buttons[i].shape.fillColor = MEDIUMGREY
                self.panel.buttons[i].draw()
            button.shape.fillColor = GREEN
            button.draw()
            callback(button.text.strip())

        self.panel = Panel(
            "select-stimulus",
            "stimulus type",
            pos,
            [480, 70],
            buttons=[
                Button(
                    "stimtype-drifting-grating",
                    "drifting grating",
                    WHITE,
                    GREEN,
                    [-145, 0],
                    padding=5,
                    onClick=onClick,
                ),
                Button(
                    "stimtype-static-grating",
                    "static grating",
                    WHITE,
                    MEDIUMGREY,
                    [17, 0],
                    padding=5,
                    onClick=onClick,
                ),
                Button(
                    "stimtype-movie",
                    "    movie   ",
                    WHITE,
                    MEDIUMGREY,
                    [160, 0],
                    padding=5,
                    onClick=onClick,
                ),
            ],
        )

    def register(self, window):
        self.panel.register(window)

    def draw(self):
        self.panel.draw()

    def contains(self, x):
        return self.panel.contains(x)

    def handleClick(self, mouse):
        self.panel.handleClick(mouse)
