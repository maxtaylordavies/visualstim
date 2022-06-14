DEFAULT_SCREEN_PARAMS = {
    "width": 518,
    "height": 523,
    "h res": 1400,
    "v res": 900,
    "dist": 300,
    "warp": False,
}
DEFAULT_STIMULUS_PARAMS = {
    "spat freq": 0.1,
    "temp freq": 0.2,
    "orientation": 0.0,
    "stim duration": 10.0,
    "filename": "test.mp4",
    "fit screen": False,
    "scale": 0.02,
    "sparseness": 0.7,
}
STIMULUS_PARAMETER_MAP = {
    "static grating": {"spat freq", "orientation", "stim duration"},
    "drift grating": {"spat freq", "temp freq", "orientation", "stim duration",},
    "osc grating": {"spat freq", "temp freq", "orientation", "stim duration",},
    "sparse noise": {"temp freq", "scale", "sparseness", "stim duration"},
    "checkerboard": {"temp freq", "scale", "stim duration"},
    "movie": {"filename", "fit screen", "stim duration"},
}
UNITS_MAP = {
    "width": "mm",
    "height": "mm",
    "h res": "pix",
    "v res": "pix",
    "dist": "mm",
    "spat freq": "cyc/deg",
    "temp freq": "Hz",
    "orientation": "deg",
    "stim duration": "s",
    "trigger duration": "s",
    "sync interval": "frames",
    "pulse length": "frames",
}
CYCLEABLE_PARAMETERS = {"spat freq", "temp freq", "orientation"}

# colors
TRANSPARENT = [0, 0, 0, 0]
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
MEDIUMGREEN = [145, 248, 212]

# these two in pixels
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900

# these three in mm
DISP_WIDTH = 518
DISP_HEIGHT = 323
DISP_DISTANCE = 300

# DEG_PER_PIX = degrees(atan2(DISP_HEIGHT / 2, DISP_DISTANCE)) / (WINDOW_HEIGHT / 2)

PIXEL_SIZE = DISP_WIDTH / WINDOW_WIDTH

DEFAULT_BACKGROUND_COLOR = WHITE
STIMULATION_BACKGROUND_COLOR = GREY

COMPRESSION_FACTOR = 2
