from typing import Any, List

from psychopy.visual import Window, TextBox2

from src.components.core import Component
from src.constants import BLACK, WHITE


class Textbox(Component):
    def __init__(
        self,
        *args,
        text: str,
        fontSize=18,
        bold=False,
        padding=5,
        borderColor=None,
        borderWidth=0,
        opacity=1,
        editable=False,
        clickable=False,
        **kwargs
    ):
        super().__init__(*args, clickable=clickable, **kwargs)
        self.text = text
        self.fontSize = fontSize
        self.bold = bold
        self.padding = padding
        self.borderColor = borderColor
        self.borderWidth = borderWidth
        self.opacity = opacity
        self.editable = editable

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

    def toggleFocus(self):
        self.children[0].hasFocus = not self.children[0].hasFocus

    def deleteCaret(self, direction="left"):
        if direction == "left":
            self.children[0].deleteCaretLeft()
        else:
            self.children[0].deleteCaretRight()

