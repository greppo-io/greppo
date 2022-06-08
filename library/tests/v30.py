from greppo import app

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

# app.image_layer(
#     image='tests/data/sfo.jpg',
#     bounds=[
#         [14.760840184106792, 77.97900023926854],
#         [14.763995704693206, 77.98389492733145],
#     ],
#     name='This name',
#     description='Some description',
#     visible=True,
# )

app.image_layer(
    image='tests/data/rvrnbrt.TIF',
    bounds=[
        [14.760840184106792, 77.97900023926854],
        [14.763995704693206, 77.98389492733145],
    ],
    name='This name',
    description='Some description',
    visible=True,
)