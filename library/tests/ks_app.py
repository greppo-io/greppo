from greppo import app
import geopandas as gpd
import numpy as np 

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

image_files = gpd.read_file("tests/data/ks_files.geojson")
image_files_titles = image_files['title'].to_list()
next_select = app.select(name="Select the next image to label",
                         options=image_files_titles, default=image_files_titles[0])

selected_image = image_files.loc[image_files['title'] == next_select]

app.image_layer(
    file_path="tests/data/" + selected_image.iloc[0]['file'],
    title=selected_image.iloc[0]['title'],
    description=selected_image.iloc[0]['description'],
    visible=True,
)

polygon_feature = gpd.GeoDataFrame(columns=['geometry'], geometry='geometry')
# polygon_feature = selected_image
draw_feature_point = app.draw_feature(
    name="Draw polygon features", features=polygon_feature, geometry=["Polygon"]
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
    backgroundColor="rgb(200, 50, 150)",
)
