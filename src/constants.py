COLORS = {
    "transparent": [0, 0, 0, 0],
    "black": [0, 0, 0],
    "white": [255, 255, 255],
    "grey": [127, 127, 127],
    "lightgrey": [230, 230, 230],
    "mediumgrey": [190, 190, 190],
    "darkgrey": [119, 119, 119],
    "green": [0, 199, 129],
    "yellow": [255, 170, 21],
    "red": [255, 64, 64],
    "purple": [125, 76, 219],
    "palegreen": [205, 255, 237],
    "palered": [255, 207, 207],
    "mediumgreen": [145, 248, 212],
}

COMPRESSION_FACTOR = 2

DEFAULT_SCREEN_PARAMS = {
    "width": 518,
    "height": 523,
    "h res": 1400,
    "v res": 900,
    "dist": 300,
    "warp": False,
    "background": "grey",
    "blank": True,
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
