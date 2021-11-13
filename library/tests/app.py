import geopandas as gpd
import numpy as np
import pandas as pd
from greppo import app

data_gdf_1 = gpd.read_file("tests/data/communes.geojson")
# data_gdf_2 = gpd.read_file("tests/data/us-states.geojson")

num_val = 10
number_1 = app.number(value=num_val, name="Number input 1")

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

# app.base_layer(
#     name="Open Street Map",
#     visible=False,
#     url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
#     subdomains=None,
#     attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
# )

# data_gdf_1["Value"] = pd.Series(
#     np.ones(len(data_gdf_1["code"])) * number_1, index=data_gdf_1.index
# )
app.overlay_layer(
    data_gdf_1,
    title="Communes",
    description="Communes in Normandy, France",
    style={"fillColor": "#F87979"},
    visible=True,
)

# data_gdf_2["MultiID"] = data_gdf_2["id"] * number_1
# app.overlay_layer(
#     data_gdf_2,
#     title="States",
#     description="States in USA",
#     style={"fillColor": "#F87979"},
#     visible=True,
# )

text_1 = app.text(value="here is a text", name="Text input 1")
select1 = app.select(name="First selector", options=["a", "b", "c"], default="a")
multiselect1 = app.multiselect(
    name="Second selector", options=["Asia", "Africa", "Europe"], default=["Asia"]
)

"""
Testing to implement the draw feature.

The input should be a gdf.
"""
# random_draw_features = gpd.read_file("tests/data/features.geojson")
# draw_feature_input = app.draw_feature(
#     name="Draw random features", features=random_draw_features
# )

line_feature = gpd.read_file("tests/data/line.geojson")
draw_feature_line = app.draw_feature(
    name="Draw line features", features=line_feature, geometry=['LineString']
)

point_feature = gpd.read_file("tests/data/point.geojson")
draw_feature_point = app.draw_feature(
    name="Draw point features", features=point_feature, geometry=['Point', 'LineString']
)

polygon_feature = gpd.read_file("tests/data/polygon.geojson")
draw_feature_polygon = app.draw_feature(
    name="Draw polygon features", features=polygon_feature, geometry=['Polygon']
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

y = []
for i in range(10, 0, -1):
    y.append(np.random.randint(0, 100))

app.bar_chart(
    name="some-name",
    title="some_title",
    description="some_chart",
    x=[i for i in range(10)],
    y=y,
)
