from greppo import app
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform
from rasterio.warp import reproject

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

# file_path = 'tests/data/rvrnbrt.TIF'
# src_dataset = rasterio.open(file_path)
# dst_crs = "EPSG:4326"

# transform, width, height = calculate_default_transform(
#     src_dataset.crs,
#     dst_crs,
#     src_dataset.width,
#     src_dataset.height,
#     *src_dataset.bounds
# )

# dst_bands = []
# for band_n_1 in range(src_dataset.count):
#     src_band = rasterio.band(src_dataset, band_n_1 + 1)
#     dst_band = reproject(src_band, dst_crs=dst_crs)
#     dst_bands.append(dst_band)

# (bounds_bottom, bounds_right) = transform * (0, 0)
# (bounds_top, bounds_left) = transform * (width, height)
# bounds = [[bounds_left, bounds_bottom], [bounds_right, bounds_top]]

# app.raster_layer(
#     data=dst_bands[0][0][0],
#     bounds=bounds,
#     name='This name',
#     description='Some description',
#     visible=True,
# )

band = np.zeros((61, 61))
band[0, :] = 1.0
band[60, :] = 1.0
band[:, 0] = 1.0
band[:, 60] = 1.0

app.raster_layer(
    data=band,
    bounds=[[0, -60], [60, 60]],
    colormap=lambda x: (1, 0, 0, x),
    name='Rectangle',
    description='A large red rectangle on a map.',
    visible=True,
)

