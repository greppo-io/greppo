from dataclasses import dataclass
from typing import List

from geopandas import GeoDataFrame as gdf


@dataclass
class RasterLayer:
    id: str
    name: str
    description: str
    url: str    
    bounds: List[List]
    visible: bool
    
    
