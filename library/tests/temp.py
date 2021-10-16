import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import json

# [{id:id, type:type, latlngs:[{lat: lat},{lng: lng}] }, {}, {}]

def frontend_dict_2_gdf(features_dict):
    features_list = []
    for feature in features_dict:
        _points = []
        _type = feature['type']
        for latlng in feature['latlngs']:
            _points.append(Point(latlng['lng'], latlng['lat']))

        if _type == 'LineString':
            feature_geom = LineString(_points)
        
        if _type == 'Polygon':
            feature_geom = Polygon(_points)
        
        if _type == 'Point':
            feature_geom = _points[0]
        
        features_list.append({'type': _type, 'geometry': feature_geom})    
    
    features_gdf = gpd.GeoDataFrame(features_list, crs="EPSG:4326")

    return features_gdf

def frontend_gdf_2_dict(features_gdf):
    features_dict = []    
    for index, feature in features_gdf.iterrows():
        _type = feature['geometry'].geom_type   
        latlngs = [] 
        if _type == 'Polygon':
            for (lng, lat) in list(feature['geometry'].exterior.coords):
                latlngs.append({'lat': lat, 'lng': lng})            
        
        if _type == 'LineString':
            for (lng, lat) in list(feature['geometry'].coords):
                latlngs.append({'lat': lat, 'lng': lng})
        
        if _type == 'Point':
            for (lng, lat) in list(feature['geometry'].coords):
                latlngs.append({'lat': lat, 'lng': lng})

        features_dict.append({'type': _type, 'latlngs': latlngs})
    return features_dict


features_gdf_0 = gpd.read_file("tests/data/features.geojson")
print(features_gdf_0.crs)
features_dict = frontend_gdf_2_dict(features_gdf_0)
# print(features_dict)
features_gdf_1 = frontend_dict_2_gdf(features_dict)
print(features_gdf_1.crs)



