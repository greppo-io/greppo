from dataclasses import dataclass
from typing import List
import uuid


@dataclass
class WMSTileLayerComponent:
    def __init__(
        self,
        url: str,
        name: str,
        visible: bool = True,
        opacity: float = 1.0,
        layers: str = '',
        subdomains: List[str] = '',
        attribution: str = '',
        transparent: bool = True,
        format: str = 'image/jpeg',
    ):
        self.url = url
        self.name = name
        self.visible = visible
        self.opacity = opacity
        self.layers = layers,
        self.subdomains = subdomains,
        self.attribution = attribution,
        self.transparent = transparent,
        self.format = format,

    def convert_to_dataclass(self):
        id = uuid.uuid4().hex
        return WMSTileLayer(id=id, url=self.url, name=self.name, visible=self.visible, opacity=self.opacity, layers=self.layers, subdomains=self.subdomains, attribution=self.attribution, transparent=self.transparent, format=self.format)


@dataclass()
class WMSTileLayer:
    id: str
    url: str
    name: str
    layers: str
    visible: bool
    opacity: float
    subdomains: List[str]
    attribution: str
    transparent: bool
    format: str
