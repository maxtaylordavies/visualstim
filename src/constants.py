import json
import pathlib
import platform

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

STIMULUS_PARAMETER_MAP = {
    "static grating": {"spat freq", "orientation", "stim duration"},
    "drift grating": {"spat freq", "temp freq", "orientation", "stim duration",},
    "osc grating": {"spat freq", "temp freq", "orientation", "stim duration",},
    "sparse noise": {"temp freq", "block size", "sparseness", "stim duration"},
    "checkerboard": {"temp freq", "block size", "stim duration"},
    "movie": {"filename", "fit screen", "stim duration", "framerate"},
}

PARAMETER_UNITS_MAP = {
    "width": "mm",
    "height": "mm",
    "h res": "pix",
    "v res": "pix",
    "dist": "mm",
    "spat freq": "cyc/deg",
    "temp freq": "Hz",
    "orientation": "deg",
    "stim duration": "s",
    "block size": "pix",
    "trigger duration": "s",
    "sync interval": "frames",
    "pulse length": "frames",
    "blank": "s",
    "framerate": "Hz",
}

PARAMETER_TYPES_MAP = {
    # screen param types
    "width": int,
    "height": int,
    "h res": int,
    "v res": int,
    "dist": float,
    "background": str,
    "warp": bool,
    "blank": float,
    # sync param types
    "sync": bool,
    "trigger duration": float,
    "sync interval": int,
    "pulse length": int,
    "trackball": bool,
    # stim param types
    "spat freq": float,
    "temp freq": float,
    "orientation": float,
    "stim duration": float,
    "filename": str,
    "fit screen": bool,
    "block size": int,
    "sparseness": float,
    "framerate": float,
}

CYCLEABLE_PARAMETERS = {"spat freq", "temp freq", "orientation"}

# INTERFACE_ADDR = "192.168.0.23"
INTERFACE_ADDR = "172.20.10.4"
INTERFACE_PORT = 9000

# TRACKBALL_LISTENER_ADDR = "192.168.0.23"
TRACKBALL_LISTENER_ADDR = "172.20.10.4"
TRACKBALL_LISTENER_PORT = 9001

# TRACKBALL_ADDR = "192.168.0.21"
TRACKBALL_ADDR = "172.20.10.9"
TRACKBALL_PORT = 8888
