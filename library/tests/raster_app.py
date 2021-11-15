import geopandas as gpd
import numpy as np
import pandas as pd
from greppo import app

data_gdf_1 = gpd.read_file("tests/data/communes.geojson")

number_1 = app.number(value=10, name="Number input 1")

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

data_gdf_1["Value"] = pd.Series(
    np.ones(len(data_gdf_1["code"])) * number_1, index=data_gdf_1.index
)
app.overlay_layer(
    data_gdf_1,
    title="Communes",
    description="Communes in Normandy, France",
    style={"fillColor": "#F87979"},
    visible=True,
)

select1 = app.select(name="First selector", options=["a", "b", "c"], default="a")
multiselect1 = app.multiselect(
    name="Second selector", options=["Asia", "Africa", "Europe"], default=["Asia"]
)

app.raster_layer(file_path="rvrnbrt.TIF")
