from greppo import app
import geopandas as gpd

sfo_amenities = gpd.read_file("tests/SFO/SFO_Amenities.geojson")
amenities = list(sfo_amenities['amenity'].unique())
selected_amenities_count = dict.fromkeys(amenities, 0)

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors | Carto Tile',
)

app.overlay_layer(
    sfo_amenities,
    title="SFO Amenities",
    description="Location of some basic amenities in San Francisco",
    style={"fillColor": "#F87979"},
    visible=True,
)

default_area_selection = gpd.read_file("tests/SFO/SFO_Selection.geojson")
area_selection = app.draw_feature(
    name="Draw area selection", features=default_area_selection, geometry=["Polygon"]
)

for idx, row in area_selection.iterrows():
    selected_amenities = sfo_amenities.loc[sfo_amenities.within(
        row.at['geometry'])]
    selected_amenities_count_df = selected_amenities['amenity'].value_counts()

    for amenity in amenities:
        if(amenity in selected_amenities_count_df.index):
            selected_amenities_count[amenity] = selected_amenities_count[amenity] + \
                selected_amenities_count_df[amenity].item()

barX = list(selected_amenities_count.keys())
barY = list(selected_amenities_count.values())

app.bar_chart(
    name="amenities-sfo-select",
    title="Amenities in SFO",
    description="The count of the basic amenities within the selected area in SFO.",
    x=barX,
    y=barY,
    backgroundColor="rgb(200, 50, 150)",
)
