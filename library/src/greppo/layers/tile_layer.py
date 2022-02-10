from dataclasses import dataclass
from typing import List
import uuid


@dataclass
class TileLayerComponent:
    def __init__(
        self,
        url: str = '',
        name: str = '',
        description: str = '',
        visible: bool = True,
        opacity: float = 1.0,
    ):
        self.url = url
        self.name = name
        self.description = description
        self.visible = visible
        self.opacity = opacity

    def convert_to_dataclass(self):
        id = uuid.uuid4().hex
        return TileLayer(id=id, url=self.url, name=self.name, description=self.description, visible=self.visible, opacity=self.opacity)


@dataclass()
class TileLayer:
    id: str
    url: str
    name: str
    description: str
    visible: bool
    opacity: float
