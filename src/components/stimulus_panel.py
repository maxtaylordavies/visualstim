from typing import Any, List

from psychopy.visual import Window
from psychopy.event import Mouse

from src.constants import LIGHTGREY, MEDIUMGREY, GREEN, WHITE
from src.components.core import Component, Panel, Button


class StimulusPanel(Component):
    def __init__(self, *args, callback: Any, **kwargs) -> None:
        super().__init__(*args, **kwargs)

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
            labelText="stimulus type",
            pos=self.pos,
            children=[
                Button(
                    self.window,
                    "stimtype-static-grating",
                    text="  static grating",
                    color=WHITE,
                    fill=MEDIUMGREY,
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-drift-grating",
                    text="   drift grating",
                    color=WHITE,
                    fill=GREEN,
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-osc-grating",
                    text="    osc grating",
                    color=WHITE,
                    fill=MEDIUMGREY,
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-movie",
                    text="       movie",
                    color=WHITE,
                    fill=MEDIUMGREY,
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-sparse-noise",
                    text="  sparse noise",
                    color=WHITE,
                    fill=MEDIUMGREY,
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
                Button(
                    self.window,
                    "stimtype-checkerboard",
                    text=" checkerboard",
                    color=WHITE,
                    fill=MEDIUMGREY,
                    pos=self.pos,
                    padding=4,
                    onClick=onClick,
                ),
            ],
            rows=2,
            padding=10,
            fill=LIGHTGREY,
        )
        self.children = [self.panel]
