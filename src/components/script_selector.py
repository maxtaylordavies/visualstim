import pathlib
import os
from typing import Any, List

from psychopy.visual import Window

from src.components.core import Button, Component, Panel
from src.constants import WHITE, GREEN, MEDIUMGREY


class ScriptSelector(Component):
    def __init__(self, window: Window, id: str, pos: List[int], callback: Any) -> None:
        super().__init__(window, id, pos)
        self.callback = callback

        expDirPath = pathlib.Path().resolve().joinpath("experiments")
        self.filenames = [
            f
            for f in os.listdir(expDirPath)
            if os.path.isfile(expDirPath.joinpath(f)) and f.endswith(".json")
        ]

        self.selected = ""

    def makeFunc(self, filename):
        return lambda a, b: self.onFileClicked(filename, a, b)

    def onFileClicked(self, filename, a, b):
        self.selected = filename
        self.register()
        self.callback(self.selected)

    def register(self):
        self.children = [
            Panel(
                self.window,
                f"{self.id}-panel",
                "load experiment",
                self.pos,
                [
                    Button(
                        self.window,
                        f"{self.id}-button-{i}",
                        filename.replace(".json", ""),
                        WHITE,
                        GREEN if self.selected == filename else MEDIUMGREY,
                        self.pos,
                        padding=5,
                        onClick=self.makeFunc(filename),
                    )
                    for i, filename in enumerate(self.filenames)
                ],
            )
        ]
        super().register()

