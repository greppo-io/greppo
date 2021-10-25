import geopandas as gpd
from greppo import app


app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

app.base_layer(
    name="Open Street Map",
    visible=False,
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

building_gdf = gpd.read_file("tests/data/buildings.geojson")

filter_select = app.multiselect(name="Filter building", options=["apartments", "retail", "house"], default=["house"])

filter_gdf = building_gdf[building_gdf.building == filter_select.get_value()[0]]

app.overlay_layer(
    filter_gdf,
    title="Communes",
    description="Communes in Normandy, France",
    style={"fillColor": "#F87979"},
    visible=True,
)
