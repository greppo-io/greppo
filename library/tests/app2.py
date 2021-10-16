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

number_1 = app.number(value=10, name="Number input 1")

data_gdf_1 = gpd.read_file("tests/data/communes.geojson")
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

y = []
for i in range(10, 0, -1):
    y.append(np.random.randint(0, 100))

app.line_chart(
    name="some-name",
    title="some_title",
    description="some_chart",
    x=[i for i in range(10)],
    y=y,
)
