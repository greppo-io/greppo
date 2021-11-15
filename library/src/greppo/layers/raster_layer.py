from dataclasses import dataclass
from typing import List

from geopandas import GeoDataFrame as gdf


@dataclass
class RasterLayer:
    id: str
    data: str
    bottom_left_bounds: List[float]
    top_right_bounds: List[float]
