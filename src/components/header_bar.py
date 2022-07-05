from src.components.core import Component, Button, PlayButton, Box
from src.components import ModeSelector, SaveButton

from src.constants import COLORS


class HeaderBar(Component):
    def __init__(
        self,
        *args,
        mode,
        toggleModeCallback,
        onStartClicked,
        onSaveClicked,
        onSwitchScreenClicked,
        onQuitClicked,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.mode = mode
        self.toggleModeCallback = toggleModeCallback
        self.onStartClicked = onStartClicked
        self.onSaveClicked = onSaveClicked
        self.onSwitchScreenClicked = onSwitchScreenClicked
        self.onQuitClicked = onQuitClicked
        self.fill = [252, 246, 227]
        self.size = [self.window.size[0], 48]
        self.pos = [
            0,
            (self.window.size[1] / self.window.scaleFactor) - (self.size[1] / 2),
        ]
        self.left = -self.size[0] / self.window.scaleFactor
        self.right = self.size[0] / self.window.scaleFactor

    def register(self):
        self.children = [
            Box(
                self.window,
                "headerbar-box",
                color=self.fill,
                pos=self.pos,
                size=self.size,
                children=[
                    Button(
                        self.window,
                        "logo-button",
                        text="visualstim",
                        pos=[self.left + 60, self.pos[1]],
                        color=COLORS["purple"],
                        fill=self.fill,
                    ),
                    ModeSelector(
                        self.window,
                        "mode-selector",
                        pos=[self.left + 205, self.pos[1]],
                        mode=self.mode,
                        callback=self.onToggleModeClicked,
                        fill=self.fill,
                    ),
                    PlayButton(
                        self.window,
                        "play-button",
                        16,
                        [self.right - 360, self.pos[1]],
                        self.onStartClicked,
                    ),
                    Button(
                        self.window,
                        "switch-screen-button",
                        text="switch screen",
                        color=COLORS["white"],
                        fill=COLORS["yellow"],
                        pos=[self.right - 190, self.pos[1]],
                        onClick=self.onSwitchScreenClicked,
                    ),
                    Button(
                        self.window,
                        "quit-button",
                        text="quit (esc)",
                        color=COLORS["white"],
                        fill=COLORS["red"],
                        pos=[self.right - 60, self.pos[1]],
                        onClick=self.onQuitClicked,
                    ),
                    # interactive mode components
                    SaveButton(
                        self.window,
                        pos=[self.right - 302, self.pos[1]],
                        callback=self.onSaveClicked,
                    ),
                ],
            )
        ]

        super().register()

    def onToggleModeClicked(self):
        self.mode = ("interactive", "scripting")[self.mode == "interactive"]
        self.getComponentById("save-button").toggleHidden()
        self.getComponentById("play-button").setPos(
            [self.right - 360, self.pos[1]]
            if self.mode == "interactive"
            else [self.right - 282, self.pos[1]]
        )
        self.toggleModeCallback()

