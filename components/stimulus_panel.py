from typing import Any, List

from components import Panel, Button

GREEN = [0, 199, 129]
GREY = [196, 196, 196]


class StimulusPanel:
    def __init__(self, pos: List[int], callback: Any) -> None:
        def onClick(button: Button):
            for i, b in enumerate(self.panel.buttons):
                if list(b.shape.fillColor) == GREEN:
                    self.panel.buttons[i].shape.fillColor = GREY
                self.panel.buttons[i].draw()
            button.shape.fillColor = GREEN
            button.draw()
            callback(button.text.strip())

        self.panel = Panel(
            "select-stimulus",
            "stimulus type",
            pos,
            [450, 70],
            buttons=[
                Button(
                    "stimtype-drum-grating",
                    "drum grating",
                    "white",
                    GREEN,
                    [-140, 0],
                    padding=5,
                    onClick=onClick,
                ),
                Button(
                    "stimtype-other-grating",
                    "other grating",
                    "white",
                    GREY,
                    [12, 0],
                    padding=5,
                    onClick=onClick,
                ),
                Button(
                    "stimtype-movie",
                    "    movie   ",
                    "white",
                    GREY,
                    [152, 0],
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
