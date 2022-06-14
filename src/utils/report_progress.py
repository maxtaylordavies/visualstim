import platform
from typing import Iterable

from src.window import Window
from src.components.core.textbox import Textbox
from src.constants import BLACK


class ReportProgress(object):
    def __init__(
        self, iterable: Iterable, window: Window, description: str, interval=10
    ) -> None:
        self.iterable = iterable
        self.window = window
        self.description = description
        self.len = len(self.iterable)
        self.index = 0
        self.interval = interval

        # not sure why, but (in my experience) on Mac the left edge
        # of the PsychoPy window is at -window_width/4; on Windows
        # it's at -window_width/2. Similar for bottom edge
        # so in order to correctly position the sync/trigger squares in
        # the bottom left corner, we need to check what platform we're on
        self.pos_factor = 2 if platform.system() == "Windows" else 4

        self.textbox = Textbox(
            self.window,
            "progress-message",
            text=f"{self.description}: 100%",
            color=BLACK,
            fontSize=16,
            zIndex=100,
            padding=10,
        )
        self.textbox.register()
        self.computePos()
        self.renderProgress()

    def __iter__(self):
        for obj in self.iterable:
            yield obj
            if self.index % self.interval == 0:
                self.renderProgress()
            self.index += 1

    def renderProgress(self):
        msg = (
            "done!"
            if self.index == self.len
            else f"{int(100 * (self.index / self.len))}%"
        )
        self.textbox.setText(f"{self.description}: {msg}")

        self.textbox.draw()
        self.window.flip(clearBuffer=False)

    def computePos(self):
        width, height = self.textbox.size
        self.textbox.setPos(
            [
                (self.window.size[0] / self.pos_factor) - (width / 2),
                (-self.window.size[1] / self.pos_factor) + height / 2,
            ]
        )
