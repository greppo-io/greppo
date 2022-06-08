from dataclasses import dataclass
from typing import List
import uuid
import struct
import zlib
import base64
import numpy as np


@dataclass
class RasterLayerComponent:
    def __init__(
        self,
        image: str,
        name: str,
        bounds: List[List[float]],  # [[lat_min, lon_min], [lat_max, lon_max]]
        description: str = '',
        origin: str = 'upper',
        visible: bool = True,
        opacity: float = 1.0,
        colormap=None
    ):
        self.name = name
        self.description = description
        self.visible = visible
        self.opacity = opacity
        assert origin in [
            "upper", "lower"], "origin should be one of `upper` or `lower`"

        if 'ndarray' in image.__class__.__name__:
            img = _write_png(image, origin=origin, colormap=colormap)
            b64encoded = base64.b64encode(img).decode('utf-8')
            self.url = 'data:image/png;base64,{}'.format(
                b64encoded).replace('\n', ' ')
        else:
            assert False, "raster data not of right format"

        assert ((len(bounds) == 2) and (len(bounds[0]) == 2) and (
            len(bounds[1]) == 2)), "bounds not of format `[[lat_min, lon_min], [lat_max, lon_max]]`"
        self.bounds = bounds

    def convert_to_dataclass(self):
        id = uuid.uuid4().hex
        return RasterLayer(id=id, url=self.url, bounds=self.bounds, name=self.name, description=self.description, visible=self.visible, opacity=self.opacity)


@dataclass
class RasterLayer:
    id: str
    url: str
    name: str
    description: str
    bounds: List[List]
    visible: bool
    opacity: float


def _write_png(data, origin='upper', colormap=None):
    """
    Taken from:
    https://github.com/python-visualization/folium/blob/551b2420150ab56b71dcf14c62e5f4b118caae32/folium/utilities.py#L156
    
    Transform an array of data into a PNG string.
    This can be written to disk using binary I/O, or encoded using base64
    for an inline PNG like this:
    >>> png_str = write_png(array)
    >>> "data:image/png;base64,"+png_str.encode('base64')
    Inspired from
    https://stackoverflow.com/questions/902761/saving-a-numpy-array-as-an-image
    Parameters
    ----------
    data: numpy array or equivalent list-like object.
         Must be NxM (mono), NxMx3 (RGB) or NxMx4 (RGBA)
    origin : ['upper' | 'lower'], optional, default 'upper'
        Place the [0,0] index of the array in the upper left or lower left
        corner of the axes.
    colormap : callable, used only for `mono` image.
        Function of the form [x -> (r,g,b)] or [x -> (r,g,b,a)]
        for transforming a mono image into RGB.
        It must output iterables of length 3 or 4, with values between
        0. and 1.  Hint: you can use colormaps from `matplotlib.cm`.
    Returns
    -------
    PNG formatted byte string
    """
    if colormap is None:
        def colormap(x):
            return (x, x, x, 1)

    arr = np.atleast_3d(data)
    height, width, nblayers = arr.shape

    if nblayers not in [1, 3, 4]:
        raise ValueError('Data must be NxM (mono), '
                         'NxMx3 (RGB), or NxMx4 (RGBA)')
    assert arr.shape == (height, width, nblayers)

    if nblayers == 1:
        arr = np.array(list(map(colormap, arr.ravel())))
        nblayers = arr.shape[1]
        if nblayers not in [3, 4]:
            raise ValueError('colormap must provide colors of r'
                             'length 3 (RGB) or 4 (RGBA)')
        arr = arr.reshape((height, width, nblayers))
    assert arr.shape == (height, width, nblayers)

    if nblayers == 3:
        arr = np.concatenate((arr, np.ones((height, width, 1))), axis=2)
        nblayers = 4
    assert arr.shape == (height, width, nblayers)
    assert nblayers == 4

    # Normalize to uint8 if it isn't already.
    if arr.dtype != 'uint8':
        with np.errstate(divide='ignore', invalid='ignore'):
            arr = arr * 255./arr.max(axis=(0, 1)).reshape((1, 1, 4))
            arr[~np.isfinite(arr)] = 0
        arr = arr.astype('uint8')

    # Eventually flip the image.
    if origin == 'lower':
        arr = arr[::-1, :, :]

    # Transform the array to bytes.
    raw_data = b''.join([b'\x00' + arr[i, :, :].tobytes()
                         for i in range(height)])

    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return (struct.pack('!I', len(data)) +
                chunk_head +
                struct.pack('!I', 0xFFFFFFFF & zlib.crc32(chunk_head)))

    return b''.join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack('!2I5B', width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(raw_data, 9)),
        png_pack(b'IEND', b'')])
