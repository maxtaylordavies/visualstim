from psychopy import event


def checkForEsc():
    return "escape" in event.getKeys()


def noOp(args):
    return