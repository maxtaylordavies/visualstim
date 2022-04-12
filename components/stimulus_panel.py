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
                    [pos[0] - 145, pos[1]],
                    padding=5,
                    onClick=onClick,
                ),
                Button(
                    "stimtype-static-grating",
                    "static grating",
                    WHITE,
                    MEDIUMGREY,
                    [pos[0] + 17, pos[1]],
                    padding=5,
                    onClick=onClick,
                ),
                Button(
                    "stimtype-movie",
                    "    movie   ",
                    WHITE,
                    MEDIUMGREY,
                    [pos[0] + 160, pos[1]],
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

    def onClick(self, mouse):
        self.panel.onClick(mouse)
