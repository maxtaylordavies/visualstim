from typing import Any, List

from psychopy.event import Mouse

from src.constants import COLORS


class Component:
    def __init__(
        self,
        window: Any,
        id: str,
        pos: List[int] = [0, 0],
        size: List[Any] = [None, None],
        color: List[int] = COLORS["black"],
        fill: List[int] = COLORS["white"],
        zIndex: int = 0,
        children: List[Any] = [],
        onClick=None,
        hide=False,
        clickable=True,
        listenForKeyPresses=False,
    ) -> None:
        self.window = window
        self.id = id
        self.pos = pos
        self.size = size
        self.color = color
        self.fill = fill
        self.zIndex = zIndex
        self.children = children
        self.onClickFallback = onClick
        self.hide = hide
        self.clickable = clickable
        self.listenForKeyPresses = listenForKeyPresses

        if self.listenForKeyPresses:
            for i in range(len(self.children)):
                self.children[i].listenForKeyPresses = True

        if self.hide:
            for i in range(len(self.children)):
                self.children[i].hide = True

    def register(self) -> None:
        for c in self.children:
            if hasattr(c, "register"):
                c.register()

    def setHidden(self, hide, propagate=False) -> None:
        self.hide = hide
        if propagate:
            for c in self.children:
                if hasattr(c, "hide"):
                    c.hide = self.hide

    def toggleHidden(self, propagate=False) -> None:
        self.setHide(not self.hide, propagate=propagate)

    def sortChildren(self) -> List:
        return sorted(
            self.children, key=lambda x: x.zIndex if hasattr(x, "zIndex") else 0
        )

    def getComponentById(self, id: str) -> Any:
        if self.id == id:
            return self
        for c in self.children:
            if not hasattr(c, "getComponentById"):
                continue
            component = c.getComponentById(id)
            if component:
                return component
        return None

    def draw(self) -> None:
        if self.hide:
            return
        for c in self.sortChildren():
            c.draw()

    def contains(self, x: Any) -> bool:
        for c in self.children:
            if c.contains(x):
                return True
        return False

    def getSize(self):
        return self.size

    def setPos(self, pos):
        self.pos = pos
        self.register()

    def onClick(self, mouse: Mouse, component: Any) -> None:
        # get list of children sorted by decreasing zIndex
        sc = self.sortChildren()[::-1]

        # deactivate any other active components
        for c in sc:
            if not c.contains(mouse) and hasattr(c, "active") and c.active:
                c.toggle()

        # if the cursor is inside a child component and that
        # child component has an onClick function, then pass
        # the event down a level and return
        for c in sc:
            if hasattr(c, "hide") and c.hide:
                continue
            if c.contains(mouse) and hasattr(c, "onClick") and c.clickable:
                c.onClick(mouse, c)
                return

        # otherwise, handle the event at this level
        if self.onClickFallback:
            self.onClickFallback(mouse, component)

    def onKeyPress(self, key: str) -> None:
        for c in self.children:
            if isinstance(c, Component) and c.listenForKeyPresses:
                # log(f"{c.id}: {key}")
                c.onKeyPress(key)
