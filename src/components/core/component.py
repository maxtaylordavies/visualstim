from typing import Any, List

from psychopy.visual import Window
from psychopy.event import Mouse

from src.utils import noOp


class Component:
    def __init__(
        self,
        window: Window,
        id: str,
        pos: List[int] = [0, 0],
        size: List[Any] = [None, None],
        zIndex: int = 0,
        children: List[Any] = [],
        onClick=None,
    ) -> None:
        self.window = window
        self.id = id
        self.pos = pos
        self.size = size
        self.zIndex = zIndex
        self.children = children
        self.onClickFallback = onClick

    def register(self) -> None:
        for c in self.children:
            if hasattr(c, "register"):
                c.register()

    def sortChildren(self) -> List:
        return sorted(
            self.children, key=lambda x: x.zIndex if hasattr(x, "zIndex") else 0
        )

    def draw(self) -> None:
        for c in self.sortChildren():
            c.draw()

    def contains(self, x: Any) -> bool:
        for c in self.children:
            if c.contains(x):
                return True
        return False

    def getSize(self):
        return self.size

    def onClick(self, mouse: Mouse, component: Any) -> None:
        for c in self.sortChildren()[::-1]:
            if c.contains(mouse) and hasattr(c, "onClick"):
                c.onClick(mouse, c)
                return
            elif hasattr(c, "active") and c.active:
                c.toggle()
                return
        if self.onClickFallback:
            self.onClickFallback(mouse, component)

    def onKeyPress(self, key: str) -> None:
        for c in self.children:
            if hasattr(c, "onKeyPress"):
                c.onKeyPress(key)
