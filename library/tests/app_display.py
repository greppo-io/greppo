from greppo import app
import geopandas as gpd
import numpy as np

app.display(value='Greppo app with app.display', name="title")

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

app.base_layer(
    provider="OpenStreetMap Mapnik",    
)
app.base_layer(
    provider="CartoDB Positron",    
)

data_gdf = gpd.read_file("tests/data/us-states.geojson")

app.overlay_layer(
    data_gdf,
    title="States",
    description="States in USA",
    style={"fillColor": "#F87979"},
    visible=True,
)

text1 = """
## Overlay layers

Overlay layers of geojson, shp, kml, gpkg files can be imported and displayed with its data as a popover.

```python
from greppo import app

data_gdf = gpd.read_file("tests/data/us-states.geojson")

app.overlay_layer(
    data_gdf,
    title="States",
    description="States in USA",
    style={"fillColor": "#F87979"},
    visible=True,
)
```
"""
app.display(value=text1, name="text1")

y = []
for i in range(10, 0, -1):
    y.append(np.random.randint(0, 100))

app.bar_chart(
    name="Chart1",
    title="A bar chart",
    description="A bar chart plotting some random numbers from numpy.",
    x=[i for i in range(10)],
    y=y,
    backgroundColor="rgb(200, 50, 150)",
)

text2 = """
## Charts

Charts can be drawn to show the data as bar or line charts.

```python
app.bar_chart(
    name="some-name",
    title="some_title",
    description="some_chart",
    x=[i for i in range(10)],
    y=y,
    backgroundColor="rgb(200, 50, 150)",
)
```
"""
app.display(value=text2, name="text2")


text3 = """
## Display

Using app.display markdown can be displayed on the sidebar.

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## A list
- A
- B
- C

## A blockquote

> Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

```python
app.display(value=text, name="unique-name-of-text")
```
"""
app.display(value=text3, name="text3")