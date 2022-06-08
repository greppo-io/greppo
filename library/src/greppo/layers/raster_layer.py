from dataclasses import dataclass
from typing import List, Callable
import uuid
import struct
import zlib
import base64
import numpy as np
from .image_layer import ImageLayer


@dataclass
class RasterLayerComponent:
    def __init__(
        self,
        data: np.ndarray,
        name: str,
        bounds: List[List[float]],  # [[lat_min, lon_min], [lat_max, lon_max]]
        description: str = '',
        origin: str = 'upper',
        visible: bool = True,
        opacity: float = 1.0,
        colormap: Callable = None
    ):
        self.name = name
        self.description = description
        self.visible = visible
        self.opacity = opacity
        assert origin in [
            "upper", "lower"], "origin should be one of `upper` or `lower`"

        assert 'ndarray' in data.__class__.__name__, "raster data not of right format"
        img = _write_png(data, origin=origin, colormap=colormap)
        b64encoded = base64.b64encode(img).decode('utf-8')
        self.url = 'data:image/png;base64,{}'.format(
            b64encoded).replace('\n', ' ')

        assert ((len(bounds) == 2) and (len(bounds[0]) == 2) and (
            len(bounds[1]) == 2)), "bounds not of format `[[lat_min, lon_min], [lat_max, lon_max]]`"
        self.bounds = bounds

    def convert_to_dataclass(self):
        id = uuid.uuid4().hex
        return ImageLayer(id=id, url=self.url, bounds=self.bounds, name=self.name, description=self.description, visible=self.visible, opacity=self.opacity)


def _write_png(data, origin='upper', colormap=None):
    """
    Taken from:
    https://github.com/python-visualization/folium/blob/551b2420150ab56b71dcf14c62e5f4b118caae32/folium/utilities.py#L156

    Transform an array of data into a PNG string.
    
    Inspired from
    https://stackoverflow.com/questions/902761/saving-a-numpy-array-as-an-image    
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


#         src_dataset = rasterio.open(file_path)
#         dst_crs = "EPSG:4326"

#         transform, width, height = calculate_default_transform(
#             src_dataset.crs,
#             dst_crs,
#             src_dataset.width,
#             src_dataset.height,
#             *src_dataset.bounds
#         )

#         dst_bands = []
#         for band_n_1 in range(src_dataset.count):
#             src_band = rasterio.band(src_dataset, band_n_1 + 1)
#             dst_band = reproject(src_band, dst_crs=dst_crs)
#             dst_bands.append(dst_band)

#         if src_dataset.count != 3:
#             for i in range(len(dst_bands), src_dataset.count):
#                 dst_bands.append(rasterio.band(src_dataset, 1))

#         alpha = np.where(dst_bands[0][0] > 1e8, 0, 1)
#         alpha_band = list(copy.deepcopy(dst_bands[0]))
#         alpha_band[0] = alpha.astype("uint8")
#         dst_bands.append(tuple(alpha_band))

#         png_kwargs = src_dataset.meta.copy()
#         png_kwargs.update(
#             {
#                 "crs": dst_crs,
#                 "width": width,
#                 "height": height,
#                 "driver": "PNG",
#                 "dtype": rasterio.uint8,
#                 "transform": transform,
#                 "count": len(dst_bands),
#             }
#         )

#         with MemoryFile() as png_memfile:
#             with png_memfile.open(**png_kwargs) as dst_file:
#                 for i_1, dst_band in enumerate(dst_bands):
#                     dst_file.write(dst_band[0][0], i_1 + 1)

#                     dst_file.write_colormap(
#                         i_1 + 1, {0: (255, 0, 0, 255), 255: (0, 0, 0, 255)}
#                     )

#                 self.raster_image_reference.append(png_memfile.read())

#             url = (
#                 "data:image/png;base64," +
#                 base64.b64encode(png_memfile.read()).decode()
#             )
#             (bounds_bottom, bounds_right) = transform * (0, 0)
#             (bounds_top, bounds_left) = transform * (width, height)
#             bounds = [[bounds_left, bounds_bottom], [bounds_right, bounds_top]]
