from typing import Any

from psychopy.event import Mouse

from src.constants import COLORS
from src.components.core import Component, Panel, Button


class StimulusPanel(Component):
    def __init__(self, *args, callback: Any, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        def onClick(mouse: Mouse, button: Button):
            for i, c in enumerate(self.panel.children):
                if isinstance(c, Button) and list(c.fill) == COLORS["green"]:
                    self.panel.children[i].changeFill(COLORS["mediumgrey"])
                self.panel.children[i].draw()
            button.changeFill(COLORS["green"])
            button.draw()
            callback(button.text.strip())

        self.panel = Panel(
            self.window,
            self.id,
            labelText="stimulus type",
            pos=self.pos,
            children=[
                Button(
                    self.window,
                    "stimtype-static-grating",
                    text="  static grating",
                    color=COLORS["white"],
                    fill=COLORS["mediumgrey"],
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-drift-grating",
                    text="   drift grating",
                    color=COLORS["white"],
                    fill=COLORS["green"],
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-osc-grating",
                    text="    osc grating",
                    color=COLORS["white"],
                    fill=COLORS["mediumgrey"],
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-movie",
                    text="       movie",
                    color=COLORS["white"],
                    fill=COLORS["mediumgrey"],
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-sparse-noise",
                    text="  sparse noise",
                    color=COLORS["white"],
                    fill=COLORS["mediumgrey"],
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-checkerboard",
                    text=" checkerboard",
                    color=COLORS["white"],
                    fill=COLORS["mediumgrey"],
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
            ],
            rows=2,
            padding=10,
            fill=COLORS["lightgrey"],
        )
        self.children = [self.panel]
