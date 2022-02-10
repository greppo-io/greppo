from dataclasses import dataclass
from typing import List
import uuid
from click import style
from geopandas import GeoDataFrame as gdf


@dataclass
class VectorLayerComponent:
    def __init__(
        self,
        data: gdf,
        name: str,
        description: str = '',
        style: dict = {},
        visible: bool = True
    ):
        self.data = data
        self.name = name
        self.description = description
        self.style = style
        self.visible = visible

    def convert_to_dataclass(self):
        id = uuid.uuid4().hex
        gdf_bounds = self.data.total_bounds
        bounds = [[gdf_bounds[1], gdf_bounds[0]],
                  [gdf_bounds[3], gdf_bounds[2]]]
        return VectorLayer(id=id, data=self.data, name=self.name, description=self.description, style=self.style, visible=self.visible, bounds=bounds)


@dataclass
class VectorLayer:
    id: str
    data: gdf
    name: str
    description: str
    style: dict
    visible: bool
    bounds: List[List]
