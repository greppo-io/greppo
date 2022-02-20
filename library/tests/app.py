import ee
import geopandas as gpd
import numpy as np
import pandas as pd
from greppo import app

# TODO fix relative link for key file and data files

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

app.tile_layer(
    name="Open Street Map",
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    visible=False,
    description="A OSM tile layer",
)

data_gdf = gpd.read_file("tests/data/us-states.geojson")
app.overlay_layer(
    data_gdf,
    name="USA States",
    description="Boundaries of States, USA",
    style={
        "color": "#eeeeee",
        "choropleth": {
            "key_on": "density",
            "bins": [1, 10, 20, 50, 100, 200, 500, 1000],
        },
    },
    visible=True,
)

text0 = """
## EarthEngine API

* Create service account
* Authenticate/Initialize
* Perform EE operations
* Get the `ee_object`
* Pass the `ee_object` to the `app.ee_layer()`
"""
app.display(value=text0, name="text0")

email = "greppo-ee-test@greppo-earth-engine.iam.gserviceaccount.com"
key_file = "/Users/adithya/.env_keys/greppo-earth-engine-448aa3afbbdb.json"
credentials = ee.ServiceAccountCredentials(email=email, key_file=key_file)
ee.Initialize(credentials)

dem = ee.Image("USGS/SRTMGL1_003")
ee_image_object = dem.updateMask(dem.gt(0))
vis_params = {
    "min": 0,
    "max": 4000,
    "palette": ["006633", "E5FFCC", "662A00", "D8D8D8", "F5F5F5"],
}
name = "DEM"
print(vis_params)
app.ee_layer(
    ee_object=ee_image_object, vis_params=vis_params, name=name, description="EE layer"
)

app.wms_tile_layer(
    url="http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi",
    name="Weather Data",
    format="image/png",
    layers="nexrad-n0r-900913",
    description="Weather WMS tile layer",
)


text1 = """
## Input APIs

- Number input: `app.number(value=10, name="Number input 1")`
- Text input: `app.text(value="here is a text", name="Text input 1")`
- Dropdown select: `app.select(name="First selector", options=["a", "b", "c"], default="a")`
- Multi-select: `app.multiselect(name="Second selector", options=["Asia", "Africa", "Europe"], default=["Asia"])`
"""
app.display(value=text1, name="text1")

number_1 = app.number(value=10, name="Number input 1")
text_1 = app.text(value="here is a text", name="Text input 1")
select1 = app.select(name="First selector", options=["a", "b", "c"], default="a")
multiselect1 = app.multiselect(
    name="Second selector", options=["Asia", "Africa", "Europe"], default=["Asia"]
)


text2 = """
## The draw feature

```python
draw_features = gpd.read_file("data/features.geojson")
draw_feature_input = app.draw_feature(
    name="Draw random features", features=draw_features, geometry=["Point", "LineString", "Polygon"]
)
```
"""
app.display(value=text2, name="text2")

line_feature = gpd.read_file("tests/data/line.geojson")
draw_feature_line = app.draw_feature(
    name="Draw line features", features=line_feature, geometry=["LineString"]
)

point_feature = gpd.read_file("tests/data/point.geojson")
draw_feature_point = app.draw_feature(
    name="Draw point features", features=point_feature, geometry=["Point", "LineString"]
)

polygon_feature = gpd.read_file("tests/data/polygon.geojson")
draw_feature_polygon = app.draw_feature(
    name="Draw polygon features", features=polygon_feature, geometry=["Polygon"]
)

text3 = """
## Some charts to display

* Line chart
* Bar chart
"""
app.display(value=text3, name="text3")

y = []
for i in range(10, 0, -1):
    y.append(np.random.randint(0, 100))

app.line_chart(
    name="some-name",
    description="some_chart",
    x=[i for i in range(10)],
    y=y,
    color="rgb(255, 99, 132)",
)

y = []
for i in range(10, 0, -1):
    y.append(np.random.randint(0, 100))

app.bar_chart(
    name="some-name",
    description="some_chart",
    x=[i for i in range(10)],
    y=y,
    color="rgb(200, 50, 150)",
)
