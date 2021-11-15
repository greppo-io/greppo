import geopandas as gpd
import numpy as np
import pandas as pd
from greppo import app

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

data_gdf_1 = gpd.read_file("tests/data/buildings.geojson")

app.overlay_layer(
    data_gdf_1,
    title="Buildings",
    description="Buildings in Rivierenbuurt, Amsterdam",
    style={"fillColor": "#F87979"},
    visible=True,
)

app.raster_layer(file_path="tests/data/rvrnbrt.TIF", title="DEM",
                 description="Digital elevation mapping of Amsterdam", visible=True)
