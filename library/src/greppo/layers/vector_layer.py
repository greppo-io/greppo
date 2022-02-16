from dataclasses import dataclass
from typing import List, Union
import uuid
from click import style
from geopandas import GeoDataFrame as gdf
from numpy import arange
from ..colorbrewer import get_palette


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

        if 'choropleth' in style:
            choropleth_style = style['choropleth']
            if 'key_on' not in choropleth_style:
                raise ValueError(
                    '"key_on" not specified in style: "choropleth" for vector_layer')
            else:
                key_on = choropleth_style['key_on']
            if key_on in data:
                choropleth_on_data = data[key_on]
            else:
                raise ValueError(
                    f'"{key_on}" is an invalid key for the passed in DataFrame')
            bin_min = choropleth_on_data.min()
            bin_max = choropleth_on_data.max()
            if 'bins' in choropleth_style:
                bins = choropleth_style['bins']
                if isinstance(bins, int):
                    if bins <= 0:
                        ValueError(
                            f'"{bins}" is a invalid for "bins" in style: "choropleth", "bins" must be >= 1')
                    bin_step = (bin_min+bin_max)/bins
                    bins = list(arange(bin_min, bin_max, bin_step))
                    choropleth_style['bins'] = bins
                elif isinstance(bins, List):
                    if not all(bin_min <= x <= bin_max for x in bins[1:]):
                        raise ValueError(
                            'Values in "bins" do not match the values in the DataFrame')
                    if not all(x <= y for x, y in zip(bins[:-1], bins[1:])):
                        raise ValueError('Values in "bins" are not increasing')
            else:
                bin_step = (bin_min+bin_max)/6
                bins = list(arange(bin_min, bin_max, bin_step))
                choropleth_style['bins'] = bins
            bins_length = len(bins)
            if 'palette' in choropleth_style:
                if isinstance(choropleth_style['palette'], str):
                    choropleth_style['palette'] = get_palette(
                        bins_length, choropleth_style['palette'])
                elif isinstance(choropleth_style['palette'], List[str]):
                    if bins_length == len(choropleth_style['palette']):
                        pass
                        # TODO Check if each item is a valid color Hex or RGB code.
                    else:
                        raise ValueError(
                            '"bins" length and "palette" length must match')
            else:
                choropleth_style['palette'] = get_palette(bins_length, 'Purples')

            choropleth_style['bins'] = list(reversed(choropleth_style['bins'])) 
            choropleth_style['palette'] = list(reversed(choropleth_style['palette'])) 
            self.style['choropleth'] = choropleth_style

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
