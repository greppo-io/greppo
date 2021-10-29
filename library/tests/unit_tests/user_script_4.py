import geopandas as gpd
from greppo import app

filter_select = app.multiselect(name="Filter building", options=["apartments", "retail", "house"], default=["house"])
