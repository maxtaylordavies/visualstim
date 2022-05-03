DEFAULT_PARAMS = {
    "stimulus": {
        "spatial frequency": 0.1,
        "temporal frequency": 0.4,
        "orientation": 0.0,
        "stimulus duration": 10.0,
        "filename": "test.mp4",
        "fit screen": False,
    },
    "sync": {
        "sync": False,
        "trigger duration": 5.0,
        "sync interval": 60,
        "pulse length": 3,
    },
}
STIMULUS_PARAMETER_MAP = {
    "drifting grating": [
        "spatial frequency",
        "temporal frequency",
        "orientation",
        "stimulus duration",
    ],
    "static grating": ["spatial frequency", "orientation", "stimulus duration"],
    "movie": ["stimulus duration", "filename", "fit screen"],
}

BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREY = [127, 127, 127]
LIGHTGREY = [230, 230, 230]
MEDIUMGREY = [190, 190, 190]
DARKGREY = [119, 119, 119]
GREEN = [0, 199, 129]
YELLOW = [255, 170, 21]
RED = [255, 64, 64]
PURPLE = [125, 76, 219]
PALEGREEN = [205, 255, 237]
PALERED = [255, 207, 207]

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900
DISP_WIDTH = 518
DISP_HEIGHT = 323
PIXEL_SIZE = DISP_WIDTH / WINDOW_WIDTH

DEFAULT_BACKGROUND_COLOR = WHITE
STIMULATION_BACKGROUND_COLOR = GREY
