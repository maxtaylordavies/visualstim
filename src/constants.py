import json
import pathlib

with open(pathlib.Path().resolve().joinpath("experiments/default.json")) as f:
    data = json.load(f)
    DEFAULT_SCREEN_PARAMS = data["screen settings"]
    DEFAULT_SYNC_PARAMS = data["sync settings"]
    DEFAULT_STIMULUS_PARAMS = data["stimuli"][0]["params"]


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
    "blank": "s",
}
CYCLEABLE_PARAMETERS = {"spat freq", "temp freq", "orientation"}
