import geopandas as gpd
from greppo import app

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

regions = gpd.read_file("tests/italy-dataset/regions_italy.geojson")
roads = gpd.read_file("tests/italy-dataset/roads_italy.geojson")
cities = gpd.read_file("tests/italy-dataset/cities_italy.geojson")

app.overlay_layer(
    regions,
    title="Regions",
    description="Regions in Italy",
    style={"fillColor": "#F87979"},
    visible=False,
)

app.overlay_layer(
    roads,
    title="Roads",
    description="Major highway roads in Italy",
    style={"fillColor": "#F87979"},
    visible=False,
)

app.overlay_layer(
    cities,
    title="Cities",
    description="Cities in Italy",
    style={"fillColor": "#F87979"},
    visible=True,
)