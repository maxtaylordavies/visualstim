from src.components.core import Component, Button, PlayButton, Box
from src.components import ModeSelector, SaveButton

from src.constants import WHITE, YELLOW, PURPLE, RED, LIGHTGREY


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

    def register(self):
        self.children = [
            Box(
                self.window,
                "headerbar-box",
                color=self.fill,
                pos=[0, 302],
                size=[self.window.size[0], 48],
                children=[
                    Button(
                        self.window,
                        "logo-button",
                        text="visualstim v0.1",
                        pos=[-420, 302],
                        color=PURPLE,
                        fill=self.fill,
                    ),
                    ModeSelector(
                        self.window,
                        "mode-selector",
                        pos=[-257, 302],
                        mode=self.mode,
                        callback=self.onToggleModeClicked,
                        fill=self.fill,
                    ),
                    PlayButton(
                        self.window, "play-button", 16, [150, 302], self.onStartClicked,
                    ),
                    Button(
                        self.window,
                        "switch-screen-button",
                        text="switch screen",
                        color=WHITE,
                        fill=YELLOW,
                        pos=[315, 302],
                        onClick=self.onSwitchScreenClicked,
                    ),
                    Button(
                        self.window,
                        "quit-button",
                        text="quit (esc)",
                        color=WHITE,
                        fill=RED,
                        pos=[440, 302],
                        onClick=self.onQuitClicked,
                    ),
                    # interactive mode components
                    SaveButton(
                        self.window, pos=[206, 302], callback=self.onSaveClicked
                    ),
                ],
            )
        ]

        super().register()

    def onToggleModeClicked(self):
        self.mode = ("interactive", "scripting")[self.mode == "interactive"]
        self.getComponentById("save-button").toggleHidden()
        self.getComponentById("play-button").setPos(
            [150, 302] if self.mode == "interactive" else [225, 302]
        )
        self.toggleModeCallback()

