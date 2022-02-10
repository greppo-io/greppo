from dataclasses import dataclass
from typing import List

from geopandas import GeoDataFrame as gdf


@dataclass
class OverlayLayer:
    id: str
    data: gdf
    name: str
    description: str
    style: dict
    visible: bool
    viewzoom: List
