from dataclasses import dataclass
from typing import List, Union, Dict
from .tile_layer import TileLayer
import ee
import uuid


@dataclass
class EarthEngineLayerComponent:
    def __init__(
        self,
        ee_object: Union[ee.Image, ee.ImageCollection, ee.FeatureCollection, ee.Feature, ee.Geometry],
        name: str = '',
        visible: bool = True,
        vis_params: Dict = {},
        opacity: float = 1.0,
        min_zoom: int = 0,
        max_zoom: int = 24
    ):
        self.name = name
        self.visible = visible
        self.opacity = opacity
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

        if (
            isinstance(ee_object, ee.geometry.Geometry)
            or isinstance(ee_object, ee.feature.Feature)
            or isinstance(ee_object, ee.featurecollection.FeatureCollection)
        ):
            features = ee.FeatureCollection(ee_object)

            width = vis_params.get('width', 2)
            color = vis_params.get('color', '000000')

            image_fill = features.style(**{"fillColor": color}).updateMask(
                ee.Image.constant(0.5)
            )
            image_outline = features.style(
                **{"color": color, "fillColor": "00000000", "width": width}
            )

            self.ee_object_image = image_fill.blend(image_outline)
        elif isinstance(ee_object, ee.image.Image):
            self.ee_object_image = ee_object
        elif isinstance(ee_object, ee.imagecollection.ImageCollection):
            self.ee_object_image = ee_object.mosaic()

        self.vis_params = vis_params

    def convert_to_dataclass(self):
        id = uuid.uuid4().hex
        map_id_dict = ee.Image(self.ee_object_image).getMapId(self.vis_params)
        url = map_id_dict["tile_fetcher"].url_format
        return TileLayer(id=id, url=url, name=self.name, visible=self.visible, opacity=self.opacity, min_zoom=self.min_zoom, max_zoom=self.max_zoom)
