from typing import List

from psychopy.visual import rect, Window

from src.components.core import Component
from .textbox import Textbox
from src.constants import WHITE
from src.utils import log


class Box(Component):
    def __init__(
        self,
        window: Window,
        id: str,
        color: List[int],
        pos: List[int],
        size: List[int],
        borderColor: List[int] = WHITE,
        borderWidth: int = 0,
        children: List[Component] = [],
        onClick=None,
    ) -> None:
        super().__init__(
            window, id, pos=pos, size=size, children=children, onClick=onClick
        )
        self.color = color
        self.borderColor = borderColor
        self.borderWidth = borderWidth

    def register(self):
        self.children = [
            Textbox(
                self.window,
                self.id,
                self.pos,
                "",
                fill=self.color,
                size=self.size,
                borderColor=self.borderColor,
                borderWidth=self.borderWidth,
            )
        ] + self.children
        super().register()

    def changeColor(self, color: List[int], draw=True):
        self.color = color
        self.children[0].fillColor = self.color
        if draw:
            self.draw()
