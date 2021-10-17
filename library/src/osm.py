"""OpenStreetMap utilities Python.

Modified version of github.com/rossant/smopy .
"""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import logging

import numpy as np

# -----------------------------------------------------------------------------
# OSM functions
# -----------------------------------------------------------------------------
def correct_box(box, z):
    """Get good box limits"""
    x0, y0, x1, y1 = box
    new_x0 = max(0, min(x0, x1))
    new_x1 = min(2 ** z - 1, max(x0, x1))
    new_y0 = max(0, min(y0, y1))
    new_y1 = min(2 ** z - 1, max(y0, y1))

    return (new_x0, new_y0, new_x1, new_y1)


def get_box_size(box):
    """Get box size"""
    x0, y0, x1, y1 = box
    sx = abs(x1 - x0) + 1
    sy = abs(y1 - y0) + 1
    return (sx, sy)


# -----------------------------------------------------------------------------
# Functions related to coordinates
# -----------------------------------------------------------------------------
def deg2num(latitude, longitude, zoom, do_round=True):
    """Convert from latitude and longitude to tile numbers.

    If do_round is True, return integers. Otherwise, return floating point
    values.

    Source: http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames#Python

    """
    lat_rad = np.radians(latitude)
    n = 2.0 ** zoom
    if do_round:
        f = np.floor
    else:
        f = lambda x: x
    xtile = f((longitude + 180.0) / 360.0 * n)
    ytile = f((1.0 - np.log(np.tan(lat_rad) + (1 / np.cos(lat_rad))) / np.pi) / 2.0 * n)
    if do_round:
        if isinstance(xtile, np.ndarray):
            xtile = xtile.astype(np.int32)
        else:
            xtile = int(xtile)
        if isinstance(ytile, np.ndarray):
            ytile = ytile.astype(np.int32)
        else:
            ytile = int(ytile)
    return (xtile, ytile)


def get_tile_box(box_latlon, z):
    """Convert a box in geographical coordinates to a box in
    tile coordinates (integers), at a given zoom level.

    box_latlon is lat0, lon0, lat1, lon1.

    """
    lat0, lon0, lat1, lon1 = box_latlon
    x0, y0 = deg2num(lat0, lon0, z)
    x1, y1 = deg2num(lat1, lon1, z)
    return (x0, y0, x1, y1)


def _box(*args):
    """Return a tuple (lat0, lon0, lat1, lon1) from a coordinate box that
    can be specified in multiple ways:

    A. box((lat0, lon0))  # nargs = 1
    B. box((lat0, lon0, lat1, lon1))  # nargs = 1
    C. box(lat0, lon0)  # nargs = 2
    D. box((lat0, lon0), (lat1, lon1))  # nargs = 2
    E. box(lat0, lon0, lat1, lon1)  # nargs = 4

    """
    nargs = len(args)
    assert nargs in (1, 2, 4)
    pos1 = None

    # Case A.
    if nargs == 1:
        assert hasattr(args[0], "__len__")
        pos = args[0]
        assert len(pos) in (2, 4)
        if len(pos) == 2:
            pos0 = pos
        elif len(pos) == 4:
            pos0 = pos[:2]
            pos1 = pos[2:]

    elif nargs == 2:
        # Case C.
        if not hasattr(args[0], "__len__"):
            pos0 = args[0], args[1]
        # Case D.
        else:
            pos0, pos1 = args[0], args[1]

    # Case E.
    elif nargs == 4:
        pos0 = args[0], args[1]
        pos1 = args[2], args[3]

    if pos1 is None:
        pos1 = pos0

    return (pos0[0], pos0[1], pos1[0], pos1[1])


def extend_box(box_latlon, margin=0.1):
    """Extend a box in geographical coordinates with a relative margin."""
    (lat0, lon0, lat1, lon1) = box_latlon
    lat0, lat1 = min(lat0, lat1), max(lat0, lat1)
    lon0, lon1 = min(lon0, lon1), max(lon0, lon1)
    dlat = max((lat1 - lat0) * margin, 0.0005)
    dlon = max((lon1 - lon0) * margin, 0.0005 / np.cos(np.radians(lat0)))
    return (
        max(lat0 - dlat, -80),
        max(lon0 - dlon, -180),
        min(lat1 + dlat, 80),
        min(lon1 + dlon, 180),
    )


# -----------------------------------------------------------------------------
# Main Map class
# -----------------------------------------------------------------------------
class Map(object):
    def __init__(self, *args, **kwargs):
        """Create and fetch the map with a given box in geographical
        coordinates.

        """
        z = kwargs.get("z", 18)
        margin = kwargs.get("margin", 0.05)

        self.tilesize = kwargs.get("tilesize", 256)
        self.maxtiles = kwargs.get("maxtiles", 16)
        self.verbose = kwargs.get("verbose", False)

        box = _box(*args)
        if margin is not None:
            box = extend_box(box, margin)
        self.box = box

        self.z = self.get_allowed_zoom(z)
        if z > self.z:
            if self.verbose:
                logging.info(
                    "Lowered zoom level to keep map size reasonable. "
                    "(z = %d)" % self.z
                )
        else:
            self.z = z

    def get_allowed_zoom(self, z=18):
        box_tile = get_tile_box(self.box, z)
        box = correct_box(box_tile, z)
        sx, sy = get_box_size(box)
        if sx * sy >= self.maxtiles:
            z = self.get_allowed_zoom(z - 1)
        return z
