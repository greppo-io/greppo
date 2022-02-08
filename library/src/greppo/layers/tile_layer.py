from dataclasses import dataclass
from typing import List
import uuid


@dataclass
class TileLayerComponent:
    def __init__(
        self,
        url: str = '',
        name: str = '',
        visible: bool = True,
        opacity: float = 1.0,
        min_zoom: int = 0,
        max_zoom: int = 24
    ):
        self.url = url
        self.name = name
        self.visible = visible
        self.opacity = opacity
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def convert_to_dataclass(self):
        id = uuid.uuid4().hex
        return TileLayer(id=id, url=self.url, name=self.name, visible=self.visible, opacity=self.opacity, min_zoom=self.min_zoom, max_zoom=self.max_zoom)


@dataclass()
class TileLayer:
    id: str
    url: str
    name: str
    visible: bool
    opacity: float
    min_zoom: int
    max_zoom: int
