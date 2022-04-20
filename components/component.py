from typing import Any

from psychopy.event import Mouse


class Component:
    def __init__(self) -> None:
        self.children = []

    def register(self) -> None:
        for c in self.children:
            c.register()

    def draw(self) -> None:
        for c in self.children:
            c.draw()

    def contains(self, x: Any) -> bool:
        for c in self.children:
            if c.contains(x):
                return True
        return False

    def onClick(self, mouse: Mouse, component: Any) -> None:
        for c in self.children:
            if c.contains(mouse) and hasattr(c, "onClick"):
                c.onClick(mouse, c)
            elif hasattr(c, "active") and c.active:
                c.toggle()

    def onKeyPress(self, key: str) -> None:
        for c in self.children:
            if hasattr(c, "onKeyPress"):
                c.onKeyPress(key)
