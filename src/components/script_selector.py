import pathlib
import os
from typing import Any

from src.components.core import Button, Component, Panel
from src.constants import LIGHTGREY, WHITE, GREEN, MEDIUMGREY


class ScriptSelector(Component):
    def __init__(self, *args, callback: Any, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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
                labelText="load experiment",
                pos=self.pos,
                children=[
                    Button(
                        self.window,
                        f"{self.id}-button-{i}",
                        text=filename.replace(".json", ""),
                        color=WHITE,
                        fill=GREEN if self.selected == filename else MEDIUMGREY,
                        pos=self.pos,
                        padding=5,
                        onClick=self.makeFunc(filename),
                    )
                    for i, filename in enumerate(self.filenames)
                ],
                fill=LIGHTGREY,
            )
        ]
        super().register()

