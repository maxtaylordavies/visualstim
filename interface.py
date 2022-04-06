from psychopy import visual, core, event

from utils import checkForEsc
from components import Button


class Interface:
    def __init__(self, components, fullscreen=False):
        self.window = visual.Window(fullscr=fullscreen, units="pix", color=[0, 0, 0])
        self.framerate = self.window.getActualFrameRate()

        def onQuitClicked(args):
            self.quit = True

        self.components = components + [
            Button("Quit", [255, 0, 0], [0, 0], onQuitClicked)
        ]
        for i in range(len(self.components)):
            self.components[i].register(self.window)

        self.mouse = event.Mouse(visible=True, win=self.window)
        self.quit = False

    def run(self):
        for component in self.components:
            component.draw()
        self.window.flip()

        clickHandled = False
        while not self.quit:
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

            # wait 0.1 seconds
            core.wait(0.1)
