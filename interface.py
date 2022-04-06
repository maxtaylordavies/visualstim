from psychopy import visual, core, event

from utils import checkForEsc
from components import Button


class Interface:
    def __init__(self, components, fullscreen=False):
        self.window = visual.Window(
            fullscr=fullscreen, units="pix", color=[255, 255, 255]
        )
        self.frameRate = self.window.getActualFrameRate()

        def onQuitClicked(args):
            self.quit = True

        self.components = components + [
            Button("visualstim v0.1", [125, 76, 219], "white", [-315, 275]),
            Button("Quit (esc)", "white", [255, 64, 64], [330, 270], onQuitClicked),
        ]
        for i in range(len(self.components)):
            self.components[i].register(self.window)

        self.mouse = event.Mouse(visible=True, win=self.window)
        self.quit = False

    def run(self):
        clickHandled = False
        while not self.quit:
            # draw components onto screen
            for component in self.components:
                component.draw()
            self.window.flip()

            # listen for click events within components
            if self.mouse.getPressed()[0]:
                for component in self.components:
                    if component.contains(self.mouse) and not clickHandled:
                        component.onClick(self)
                        clickHandled = True
            else:
                clickHandled = False

            # exit if user has pressed esc
            if checkForEsc():
                self.quit = True
