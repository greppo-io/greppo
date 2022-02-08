from greppo import app
import geopandas as gpd

import ee

"""
Authenticate earthengine-api using a Service-Account-Credential

ServiceAccountCredentials(email, key_file=None, key_data=None):

email: The email address of the account for which to configure credentials.
    Ignored if key_file or key_data represents a JSON service account key.
    email = my-service-account@...gserviceaccount.com
    email = greppo-ee-test@greppo-earth-engine.iam.gserviceaccount.com

key_file: The path to a file containing the private key associated with
    the service account. Both JSON and PEM files are supported.

key_data: Raw key data to use, if key_file is not specified.
"""



# # Compute the trend of night-time lights.

# # Adds a band containing image date as years since 1991.

# def create_time_band(img):
#     year = ee.Date(img.get('system:time_start')).get('year').subtract(1991)
#     return ee.Image(year).byte().addBands(img)


# # Map the time band creation helper over the night-time lights collection.
# # https://developers.google.com/earth-engine/datasets/catalog/NOAA_DMSP-OLS_NIGHTTIME_LIGHTS
# collection = ee.ImageCollection(
#     'NOAA/DMSP-OLS/NIGHTTIME_LIGHTS').select('stable_lights').map(create_time_band)

# # Compute a linear fit over the series of values at each pixel, visualizing
# # the y-intercept in green, and positive/negative slopes as red/blue.
# vis_params = {'min': 0, 'max': [0.18, 20, -0.18],
#               'bands': ['scale', 'offset', 'scale']}
# ee_image_object = collection.reduce(ee.Reducer.linearFit())
# map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
# ee_url = map_id_dict['tile_fetcher'].url_format

# app.base_layer(
#     name="stable lights trend",
#     visible=True,
#     url='https://earthengine.googleapis.com/v1alpha/projects/earthengine-legacy/maps/295c4c884593fb86efc53f1b1fc52ea1-6f0be59a58e33645503ec77b9d4e1a40/tiles/{z}/{x}/{y}',
#     subdomains=None,
#     attribution='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
# )

#############

email = 'greppo-ee-test@greppo-earth-engine.iam.gserviceaccount.com'
key_file = '/Users/adithya/.env_keys/greppo-earth-engine-448aa3afbbdb.json'
credentials = ee.ServiceAccountCredentials(email=email, key_file=key_file)
ee.Initialize(credentials)

dem = ee.Image('USGS/SRTMGL1_003')
ee_image_object = dem.updateMask(dem.gt(0))
vis_params = {
    'min': 0,
    'max': 4000,
    'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}
name = 'DEM'
print(vis_params)
app.ee_layer(ee_object=ee_image_object,
             vis_params=vis_params, name=name)


data_gdf_1 = gpd.read_file("tests/data/buildings.geojson")

app.vector_layer(
    data=data_gdf_1,
    title="Buildings",
    description="Buildings in Rivierenbuurt, Amsterdam",
    style={"fillColor": "#F87979"},
    visible=True,
)

app.raster_layer(file_path="tests/data/rvrnbrt.TIF", title="DEM",
                 description="Digital elevation mapping of Amsterdam", visible=True)


app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)

app.wms_tile_layer(url='http://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi', name='Weather Data', format='image/png', layers='nexrad-n0r-900913')
