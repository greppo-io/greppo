from dataclasses import dataclass
from typing import List
import numpy as np
import uuid
import io
import base64
import os
import json
from urllib.parse import urlparse, uses_netloc, uses_params, uses_relative


@dataclass
class ImageLayerComponent:
    def __init__(
        self,
        image: str,
        name: str,
        bounds: List[List[float]],  # [[lat_min, lon_min], [lat_max, lon_max]]
        description: str = '',
        visible: bool = True,
        opacity: float = 1.0,
    ):
        self.name = name
        self.description = description
        self.visible = visible
        self.opacity = opacity

        # image_ext = image.split(".")[-1].lower()
        # buffered = io.BytesIO()
        # image_open = Image.open(image)
        # image_open.save(buffered, format="JPEG")
        # image_string = base64.b64encode(buffered.getvalue()).decode()
        # self.image = f"data:image/{image_ext};base64," + image_string
        self.url = _image_to_url(image)

        assert ((len(bounds) == 2) and (len(bounds[0]) == 2) and (
            len(bounds[1]) == 2)), "bounds not of format `[[lat_min, lon_min], [lat_max, lon_max]]`"
        self.bounds = bounds

    def convert_to_dataclass(self):
        id = uuid.uuid4().hex
        return ImageLayer(id=id, url=self.url, bounds=self.bounds, name=self.name, description=self.description, visible=self.visible, opacity=self.opacity)


@dataclass
class ImageLayer:
    id: str
    url: str
    name: str
    description: str
    bounds: List[List]
    visible: bool
    opacity: float


def _image_to_url(image):
    """
    Adopted from Folium 
    https://github.com/python-visualization/folium/blob/551b2420150ab56b71dcf14c62e5f4b118caae32/folium/raster_layers.py#L187
    """
    if isinstance(image, str) and not _is_url(image):
        img_ext = os.path.splitext(image)[-1][1:]
        assert img_ext in [
            "png",
            "jpg",
            "jpeg",
            "tiff",
        ], "Image input extension should be png, jpg or jpeg for image_layer"
        with io.open(image, 'rb') as f:
            img = f.read()
        b64encoded = base64.b64encode(img).decode('utf-8')
        url = 'data:image/{};base64,{}'.format(img_ext, b64encoded)
    elif _is_url(image):
        # Round-trip to ensure a nice formatted json.
        url = json.loads(json.dumps(image))
    else:
        assert False, "image not of correct format."
    return url.replace('\n', ' ')


def _is_url(url):
    """
    Check to see if `url` has a valid protocol.

    Taken from:
    https://github.com/python-visualization/folium/blob/551b2420150ab56b71dcf14c62e5f4b118caae32/folium/utilities.py#L148
    """
    _VALID_URLS = set(uses_relative + uses_netloc + uses_params)
    _VALID_URLS.discard('')
    _VALID_URLS.add('data')

    try:
        return urlparse(url).scheme in _VALID_URLS
    except Exception:
        return False
