import json
from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Dict
from typing import List

from geopandas import GeoDataFrame as gdf
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry import Polygon


default_gdf = gdf(
    [{"id": 9999, "type": "Point", "geometry": Point(0, 0)}], crs="EPSG:4326"
)


@dataclass
class DrawFeature:
    def __init__(
        self,
        name: str,
        geometry: list,
        features: gdf = default_gdf,
        input_updates: Dict[str, Any] = {},
    ):
        self.input_name = name
        self.geometry = geometry
        # TODO Check if it matches EPSG 4326/WSG84
        self.features = features.explode(ignore_index=True)

        self.input_updates = input_updates

    def get_value(self):
        id, name = self.input_name.split("_")
        if name in self.input_updates:
            return draw_feature_dict_2_gdf(self.input_updates.get(name))

        return self.features

    def convert_to_component_info(self):
        _id, name = self.input_name.split("_")
        _type = DrawFeature.__name__
        _geometry = self.geometry
        _features = draw_feature_gdf_2_dict(self.get_value())

        return DrawFeatureComponentInfo(
            id=_id, name=name, type=_type, geometry=_geometry, features=_features
        )

    @classmethod
    def proxy_name(cls):
        return "draw_feature"

    def __repr__(self):
        return str(self.get_value())

    def __str__(self):
        return self.__repr__()


def draw_feature_dict_2_gdf(features_dict):
    features_list = []
    for feature in features_dict:
        _points = []
        _type = feature["type"]
        for latlng in feature["latlngs"]:
            _points.append(Point(latlng["lng"], latlng["lat"]))

        if _type == "LineString":
            feature_geom = LineString(_points)

        if _type == "Polygon":
            feature_geom = Polygon(_points)

        if _type == "Point":
            feature_geom = _points[0]

        features_list.append({"type": _type, "geometry": feature_geom})

    features_gdf = gdf(features_list, crs="EPSG:4326")

    return features_gdf


def draw_feature_gdf_2_dict(features_gdf):
    features_dict = []
    for index, feature in features_gdf.iterrows():
        _type = feature["geometry"].geom_type
        latlngs = []
        if _type == "Polygon":
            for (lng, lat) in list(feature["geometry"].exterior.coords):
                latlngs.append({"lat": lat, "lng": lng})

        if _type == "LineString":
            for (lng, lat) in list(feature["geometry"].coords):
                latlngs.append({"lat": lat, "lng": lng})

        if _type == "Point":
            for (lng, lat) in list(feature["geometry"].coords):
                latlngs.append({"lat": lat, "lng": lng})

        features_dict.append({"type": _type, "latlngs": latlngs})
    return features_dict


@dataclass
class DrawFeatureComponentInfo:
    id: str
    type: str
    name: str
    geometry: list
    features: dict
