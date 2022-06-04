from typing import Any, List

from psychopy.visual import Window, TextBox2

from src.components.core import Component
from src.constants import BLACK, WHITE


class Textbox(Component):
    def __init__(
        self,
        window: Window,
        id: str,
        pos: List[int],
        text: str,
        size=[None, None],
        fontSize=18,
        color=BLACK,
        fill=WHITE,
        bold=False,
        padding=5,
        borderColor=None,
        borderWidth=0,
        opacity=1,
        editable=False,
        hide=False,
        clickable=False,
    ):
        super().__init__(window, id, pos, size, hide=hide, clickable=clickable)
        self.text = text
        self.fontSize = fontSize
        self.color = color
        self.fill = fill
        self.bold = bold
        self.padding = padding
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.opacity = opacity
        self.editable = editable
        self.hide = hide

        self.children = [
            TextBox2(
                self.window,
                self.text,
                "Open Sans",
                units="pix",
                letterHeight=self.fontSize,
                colorSpace="rgb255",
                color=self.color,
                fillColor=self.fill,
                bold=self.bold,
                padding=self.padding,
                borderColor=self.borderColor,
                borderWidth=self.borderWidth,
                size=self.size,
                pos=self.pos,
                opacity=self.opacity,
                editable=self.editable,
            )
        ]

        self.size = self.children[0].size

    def setSize(self, size):
        self.size = size
        self.children[0].size = self.size

    def setPos(self, pos):
        self.pos = pos
        self.children[0].pos = self.pos

    def getText(self):
        return self.children[0].text

    def setText(self, text):
        self.text = text
        self.children[0].text = self.text

